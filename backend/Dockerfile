FROM python:3.12


WORKDIR /code


RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


COPY run_migrations.sh .


RUN chmod +x run_migrations.sh


CMD ["sh", "-c", "./run_migrations.sh && uvicorn app.main:app --host 0.0.0.0 --port 80"]