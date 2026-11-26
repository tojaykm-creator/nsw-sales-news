#!/usr/bin/env python3
"""Google News RSS -> data.json (rule-based classification, free translation, no AI credits)."""
import json, re, html, time, urllib.parse, urllib.request, datetime as dt
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

HERE = Path(__file__).parent
R = json.loads((HERE / "rules.json").read_text(encoding="utf-8"))
DATA = HERE / "data.json"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()

def classify(title, fallback):
    for c in R["cats"]:
        if c[0] == fallback and c[4] and re.search(c[4], title, re.I):
            return fallback
    for c in R["cats"]:
        if c[4] and re.search(c[4], title, re.I):
            return c[0]
    return fallback

def relevant(title, source_url):
    """Logistics topic (brand names ignored) AND Australian title or publisher."""
    host = urllib.parse.urlparse(source_url).hostname or ""
    text = re.sub(R["brands"], "", title, flags=re.I)
    return bool(re.search(R["topic"], text, re.I)
                and (re.search(R["place"], title, re.I) or host.endswith(".au")))

def enrich(title):
    stage = next((s[0] for s in R["stages"] if re.search(s[2], title, re.I)), "")
    m = re.search(r"A?\$\s?\d[\d,.]*\s?(billion|million|bn\b|b\b|m\b)?", title, re.I)
    region = next((x for x in R["regions"] if re.search(rf"\b{x}\b", title, re.I)), "")
    return stage, (m.group(0).strip() if m else ""), region

def parse(xml, cat):
    out = []
    for it in ET.fromstring(xml).iter("item"):
        title = html.unescape(it.findtext("title") or "")
        source = it.findtext("source") or ""
        if source and title.endswith(" - " + source):
            title = title[: -len(source) - 3]
        if not title or re.search(R["exclude"], title, re.I):
            continue
        src = it.find("source")
        if not relevant(title, (src.get("url") or "") if src is not None else ""):
            continue
        date = parsedate_to_datetime(it.findtext("pubDate")).astimezone(dt.timezone.utc)
        stage, amount, region = enrich(title)
        out.append(dict(title=title, ko="", url=it.findtext("link"), source=source,
                        date=date.isoformat(), cat=classify(title, cat), stage=stage,
                        amount=amount, region=region, v=3))
    return out

def mymemory(text):
    q = urllib.parse.urlencode({"q": text[:480], "langpair": "en|ko"})
    j = json.loads(get("https://api.mymemory.translated.net/get?" + q))
    if str(j.get("responseStatus")) != "200":
        raise RuntimeError(f"{j.get('responseStatus')} {j.get('responseDetails')}")
    return html.unescape(j["responseData"]["translatedText"])

def google(text):
    # unofficial free endpoint; may stop working without notice
    q = urllib.parse.urlencode({"client": "gtx", "sl": "en", "tl": "ko", "dt": "t", "q": text[:480]})
    j = json.loads(get("https://translate.googleapis.com/translate_a/single?" + q))
    return "".join(part[0] for part in j[0] if part[0])

def translate(text):
    for fn in (mymemory, google):
        try:
            out = fn(text)
            if re.search("[가-힣]", out):
                return out
            print(fn.__name__, "returned no Korean")
        except Exception as e:
            print(fn.__name__, "failed:", e)
    raise RuntimeError("all translators failed")

def main():
    old = json.loads(DATA.read_text(encoding="utf-8"))["items"] if DATA.exists() else []
    items = {i["title"].lower(): i for i in old if i.get("v") == 3}
    ok = 0
    for c in R["cats"]:
        for query in c[3]:
            time.sleep(8)  # space requests to avoid 503 blocking
            q = urllib.parse.quote(query + " when:30d")
            try:
                found = parse(get(f"https://news.google.com/rss/search?q={q}&hl=en-AU&gl=AU&ceid=AU:en"), c[0])
                ok += 1
            except Exception as e:
                print("fetch failed:", query, e)
                continue
            print(query, "->", len(found))
            for i in found[:40]:
                items.setdefault(i["title"].lower(), i)
    if not ok:
        raise SystemExit("All feeds failed; data.json left unchanged.")
    cutoff = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=30)).isoformat()
    rows = sorted((i for i in items.values() if i["date"] >= cutoff), key=lambda i: i["date"], reverse=True)[:500]
    done = fails = 0
    for i in rows:
        if i["ko"] or done >= 250 or fails >= 3:
            continue
        try:
            i["ko"] = translate(i["title"]); done += 1; fails = 0; time.sleep(0.5)
        except Exception as e:
            fails += 1; print("translation failed:", e)
    DATA.write_text(json.dumps({"updated": dt.datetime.now(dt.timezone.utc).isoformat(), "items": rows},
                               ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(rows), "items,", done, "translated")

if __name__ == "__main__":
    main()
