# Backend 테스트 개발/실행환경 구축방법 안내

# Windows Powershell 기준
관리자 권한의 Powershell 을 열고 아래의 명령어 입력(venv 사용하기 위한 설정 : https://architree9.tistory.com/7)
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
# Y 를 선택함
```

새로운 Powershell 창을 열고 아래의 명령어 입력
```
pwd
# 2024-2-SCS4031-HELLOWORLD-9 에 위치해있어야 함.

python -m venv myenv
cd backend
cd test
# 생성된 venv 안에 pip 로 의존성 설치  (myenv 폴더 삭제 시 의존성도 깔끔하게 삭제됨)
pip install -r requirements.txt

```
## OpenAI API 키 파일에 저장
https://wikidocs.net/233342 의 설명에 따라, OpenAI API 키를 얻습니다. (결제정보 입력 필요함)
얻은 API 키를 .env 파일을 생성하여 넣습니다.
형식은 .env.example 파일 참고.
```
# backend\test\.env 를 열고, 본인의 OpenAI API Key 로 교체 후, 아래 명령어 실행
cd backend\test
python openai_api_set.py

# 본인의 api 키가 출력되어야함.
```
# 테스트용 파일 다운로드
backend\test\rag_metadata_test\data\test.pdf.example 파일의 설명을 읽고, pdf 파일을 다운로드 받은 후, test.pdf.example 과 동일한 폴더에 위치시킴.

# test 스크립트 실행
```
pwd
# 2024-2-SCS4031-HELLOWORLD-9 에 위치해있어야 함.

cd backend\test\rag_metadata_test
python rag_docstore_meta_test.py

```
# 디렉토리 구조
backend
 | data
 | src
 | vectorDB
 | .env
 | requirements.txt