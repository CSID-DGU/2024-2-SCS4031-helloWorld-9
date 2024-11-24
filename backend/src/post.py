import requests

url = 'http://127.0.0.1:8000/upload-doc/'
files = {'files': open('hanhwa-testdata.pdf', 'rb')}
response = requests.post(url, files=files)

print(response.json())  # 서버의 응답 출력
