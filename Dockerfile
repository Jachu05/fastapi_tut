FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirementx.txt

COPY . .

CMD ['uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000']