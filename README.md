# 2024-2-SCS4031-helloWorld-9
RAG를 활용한 보험 문서 챗봇 만들기 프로젝트

# 실행 방법 안내 
## openai api key 설정
openai api key 를 발급받아서 입력해야함.
.env.example 파일을 수정하여 실제 키를 입력하고, 파일 이름을 .env 로 변경할 것.

## 실행 명령어
*docker 가 설치되어있어야함.
```
docker compose up
```

이후, `localhost:3000` 으로 접속

## 파일 업로드
Menu - PDF 관리 탭에서, pdf 파일을 브라우저로 드래그하거나 Add New 클릭하여 파일을 추가.
잠시 기다린 후, Menu - 챗봇 에서 질문하면 RAG 시스템 작동.

## Commit Convention
-   feat : 새로운 기능 추가
-   fix : 버그 수정
-   docs : 문서 수정
-   style : 코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우
-   refactor: 코드 리펙토링
-   test: 테스트 코드, 리펙토링 테스트 코드 추가
-   chore : 빌드 업무 수정, 패키지 매니저 수정
