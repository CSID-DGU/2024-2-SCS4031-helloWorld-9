# 2024-2-SCS4031-helloWorld-9
RAG를 활용한 보험 문서 챗봇 만들기 프로젝트

# 개발환경 세팅
Linux, MacOS
```
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirement.txt
python3 test.py # 실제 파일이름으로 변경
```
Windows
```
python -m venv myenv
source myenv/bin/activate
pip install -r requirement.txt
python3 test.py # 실제 파일이름으로 변경
```

# GitHub Role
다음과 같은 Convetion을 따릅니다.

## Commit Convention
-   feat : 새로운 기능 추가
-   fix : 버그 수정
-   docs : 문서 수정
-   style : 코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우
-   refactor: 코드 리펙토링
-   test: 테스트 코드, 리펙토링 테스트 코드 추가
-   chore : 빌드 업무 수정, 패키지 매니저 수정

## 💡 PR Convetion

| 아이콘 | 코드                       | 설명                     |
| ------ | -------------------------- | ------------------------ |
| 🎨     | :art                       | 코드의 구조/형태 개선    |
| ⚡️    | :zap                       | 성능 개선                |
| 🔥     | :fire                      | 코드/파일 삭제           |
| 🐛     | :bug                       | 버그 수정                |
| 🚑     | :ambulance                 | 긴급 수정                |
| ✨     | :sparkles                  | 새 기능                  |
| 💄     | :lipstick                  | UI/스타일 파일 추가/수정 |
| ⏪     | :rewind                    | 변경 내용 되돌리기       |
| 🔀     | :twisted_rightwards_arrows | 브랜치 합병              |
| 💡     | :bulb                      | 주석 추가/수정           |
| 🗃      | :card_file_box             | 데이버베이스 관련 수정   |


 # 기능 수정하여 github 커밋 시, 새로운 python 의존성 설치 시, requirements.txt 파일 수정 명령어
 Windows Powershell
```sh
pip freeze | Out-File -FilePath requirements.txt -Encoding UTF8
```