FROM python:3.12.5-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn

EXPOSE 8000

CMD ["uvicorn", "legacy_cms_service:app", "--host", "0.0.0.0", "--port", "8000"]