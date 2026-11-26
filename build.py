import json, pathlib, collect as c
R=c.R
def it(d,cat,en,ko,src,url,stage="",amount="",region=""):
    return dict(title=en,ko=ko,url=url,source=src,date=d+"T00:00:00+00:00",cat=cat,stage=stage,amount=amount,region=region)
seed=[
it("2026-11-18","invest","Charter Hall's $1b Light Horse hub fully leased as Woolworths takes new chilled DC","Charter Hall의 10억 달러 Light Horse 허브, Woolworths 신선센터 포함 임대 100% 완료","Prime Mover","https://primemovermag.com.au/woolworths-showcases-new-sydney-distribution-centre/","","$1b","Eastern Creek"),
it("2026-11-16","invest","Woolworths unveils automated chilled and fresh DC ahead of 2027 opening","Woolworths, 2027년 개장 예정 자동화 신선 물류센터 공개","Trailer Magazine","https://www.trailermag.com.au/woolworths-showcases-new-sydney-distribution-centre","Construction","","Eastern Creek"),
it("2026-11-16","trade","DAFF notice 195-2026: Cargo Scheduling Policy implementation update","DAFF 공지 195-2026: 화물 스케줄링 정책 시행 업데이트","DAFF","https://www.agriculture.gov.au/biosecurity-trade/import/industry-advice/2026"),
it("2026-11-04","retail","Woolworths recruiting 800 roles for Western Sydney fresh distribution centre","Woolworths, 서부 시드니 신선 물류센터 인력 800명 채용","Woolworths Group","https://www.woolworthsgroup.com.au/au/en/our-newsroom/media-releases/latest-news/2026/800-new-jobs-created-and-even-fresher-produce-for-customers-as-Woolworths-prepares-to-open-next-generation-distribution-centre.html","","","Western Sydney"),
it("2026-10-01","invest","Aldi begins construction of $1b+ automated distribution centre at Bradfield","Aldi, Bradfield에 10억 달러 이상 자동화 물류센터 착공 (2030년 개장 예정)","retailbiz","https://www.retailbiz.com.au/latest-news/aldi-1b-western-sydney-distribution-centre/","Construction","$1b+","Bradfield"),
it("2026-07-16","invest","$1b Burrah Park logistics and industrial estate approved in Western Sydney","서부 시드니 10억 달러 Burrah Park 물류·산업단지 승인","MHD","https://mhdsupplychain.com.au/2026/07/16/1-billion-western-sydney-logistics-and-industrial-hub-approved/","Approval","$1b","Western Sydney"),
it("2026-06-16","trade","DAFF: revised biosecurity diagnostic fees for imported cargo planned from 1 November 2026","DAFF: 수입화물 검역 진단 수수료 개편, 2026년 11월 1일 시행 예정으로 공지","DAFF 93-2026","https://www.agriculture.gov.au/biosecurity-trade/import/industry-advice/2026/93-2026","Announcement"),
]
tpl=pathlib.Path("template.html").read_text()
cfg={"cats":R["cats"],"stages":R["stages"]}
j=lambda o:json.dumps(o,ensure_ascii=False).replace("</","<\\/")
pathlib.Path("index.html").write_text(tpl.replace("__CFG__",j(cfg)).replace("__SEED__",j(seed)))
