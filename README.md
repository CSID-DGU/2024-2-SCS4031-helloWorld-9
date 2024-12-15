# 2024-2-SCS4031-helloWorld-9
RAG를 활용한 보험 문서 챗봇 만들기 프로젝트

# 실행 방법
### backend 구동
chatbot 서버를 실행시킵니다.
- python 이 설치되어있어야 함.
- 의존성 충돌을 피하기 위하여 가상환경(anaconda, venv) 등을 사용하는 것을 권장함.
```
pip install -r backend/requirements.txt
python backend/app.py
```
### frontend 구동
chatbot 브라우저 앱을 실행시킵니다.
- nodejs 가 설치되어있어야함.
```
npm install --prefix /frontend/chatbot-app
npm run dev
```
이후, 콘솔 터미널에 출력되는 주소로 브라우저를 통해 접속합니다.

## Commit Convention
-   feat : 새로운 기능 추가
-   fix : 버그 수정
-   docs : 문서 수정
-   style : 코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우
-   refactor: 코드 리펙토링
-   test: 테스트 코드, 리펙토링 테스트 코드 추가
-   chore : 빌드 업무 수정, 패키지 매니저 수정
