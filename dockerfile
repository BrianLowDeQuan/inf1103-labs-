FROM python:3.11-slim
WORKDIR /app
COPY smart_auditor.py .
CMD ["python", "smart_auditor.py"]