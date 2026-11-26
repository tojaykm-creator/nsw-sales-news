# NSW 영업 뉴스 앱

## 파일
- index.html : 앱 화면 (data.json 이 없으면 샘플 7건 표시)
- collect.py / rules.json : 뉴스 수집, 분류, 번역. 검색어와 키워드는 rules.json 에서 수정
- .github/workflows/collect.yml : 매시간 자동 수집
- manifest.json : 휴대폰 홈 화면 추가용
- build.py, template.html : 화면 원본 (python build.py 로 index.html 재생성)

## 설치 (GitHub)
먼저 사내 보안 정책을 확인하세요. Pages 주소는 일반적으로 누구나 볼 수 있습니다.
1. GitHub 에 새 저장소 생성
2. 압축을 푼 파일 전체 업로드 (.github 폴더 포함)
3. Settings > Actions > General > Workflow permissions : Read and write
4. Actions 탭 > collect-news > Run workflow
5. Settings > Pages > Deploy from a branch > main, /(root)
6. 휴대폰 Chrome 에서 주소를 열고 홈 화면에 추가

## 주의
- 실제 뉴스 수집과 번역은 아직 실행 테스트 전입니다.
- 무료 번역은 사용 한도가 있어, 초과하면 영어 제목이 표시됩니다.
- 분류와 단계 표시는 키워드 규칙이라 틀릴 수 있으니 원문을 확인하세요.
- 저장과 메모는 해당 브라우저에만 남습니다.
