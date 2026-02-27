FROM python:3.12.5-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Services/delivery_service/requirements.txt .
COPY Lib/lib_requirement.txt /tmp/lib_requirement.txt
RUN pip install --no-cache-dir -r requirements.txt && \
	pip install --no-cache-dir -r /tmp/lib_requirement.txt

COPY Services/delivery_service/ .
COPY Lib/ ./Lib/

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
