# ** install && execution**

## 1. .env 추가
```
DB_HOST = SAMPLE_DB_HOST
DB_USER = SAMPLE_DB_USER
DB_PASSWORD = SAMPLE_DB_PASSWORD
DB_DATABASE = SAMPLE_DB_DATABASE

REDIS_HOST = SAMPLE_REDIS_HOST
REDIS_PORT = SAMPLE_REDIS_PORT

JWT_SECRET_KEY = SAMPLE_JWT_SECRET_KEY
```
## 2. 가상환경 설정 (windows 기준)
```
$ python3 -m venv elicevenv
$ .\elicevenv\Scripts\activate
```
## 3. 필요 프로그램 설치
```
$ pip install -r requirements.txt
```
## 4. 웹서버 실행
```
$ uvicorn main:app --reload
```
## 5. 프로그램 종료 후 가상환경 종료
```
press Ctrl + C
$ deactivate
```