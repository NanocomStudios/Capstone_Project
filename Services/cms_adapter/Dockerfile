# Dockerfile for cms_adapter
FROM python:3.12.5-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Services/cms_adapter/ /app
COPY Lib/ /app/Lib/

RUN pip install --no-cache-dir fastapi uvicorn requests pydantic xmltodict
RUN pip install --no-cache-dir -r /app/Lib/lib_requirement.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]