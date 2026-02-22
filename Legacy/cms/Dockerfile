FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn

CMD ["uvicorn", "legacy_cms_service:app", "--host", "0.0.0.0", "--port", "8000"]