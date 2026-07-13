FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY data ./data

ENV EMAIL_API_HOST=0.0.0.0
ENV EMAIL_API_PORT=8000
ENV EMAIL_API_DB=/app/data/email_lab.sqlite
ENV STUDENT_ID=student-01
ENV STUDENT_EMAIL=student-01@workshop.example

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host ${EMAIL_API_HOST} --port ${EMAIL_API_PORT}"]
