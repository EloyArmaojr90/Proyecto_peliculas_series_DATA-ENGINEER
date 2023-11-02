FROM python:3.10
WORKDIR /proyecto

RUN pip install -r requirements.txt
COPY . proyecto

EXPOSE 8000

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]
