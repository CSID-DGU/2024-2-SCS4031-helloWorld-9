# Backend 개발/실행환경 구축방법 안내

## 의존성 다운로드
```
pip install -r requirements.txt
```

## OpenAI API 키 파일에 저장
https://wikidocs.net/233342 의 설명에 따라, OpenAI API 키를 얻습니다. (결제정보 입력 필요함)
얻은 API 키를 .env 파일을 생성하여 넣습니다.
형식은 .env.example 파일 참고.

## API setting 스크립트 실행
.env 파일로 부터 API 키를 운영체제의 환경변수에 저장합니다.
```
python openai_api_set.py
```

## .example 파일을 실제 파일로 교체 후, 동일한 디렉토리에 위치시킴.
주로, 외부 데이터를 다운로드해야하는 경우입니다.

## backend script 실행