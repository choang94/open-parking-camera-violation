FROM python:3.9

WORKDIR project01/app

COPY requirements.txt .
COPY src/. .

RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]