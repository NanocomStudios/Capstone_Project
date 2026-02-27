FROM python:3.12.5-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Services/service_registry/requirements.txt .
COPY Lib/lib_requirement.txt /tmp/lib_requirement.txt
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r /tmp/lib_requirement.txt

COPY Services/service_registry/ .
COPY Lib/ ./Lib/

EXPOSE 8000

CMD ["fastapi", "run", "service_registry.py", "--host", "0.0.0.0", "--port", "8000"]

RUN apt-get update && apt-get install -y curl

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1