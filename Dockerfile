FROM python:3.10
COPY requirements.txt requirements.txt
COPY settings.env settings.env

RUN pip install -r requirements.txt

EXPOSE 8000
COPY . .
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]
