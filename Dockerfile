FROM python:3.10

RUN mkdir /CFT

WORKDIR /CFT

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /CFT/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
