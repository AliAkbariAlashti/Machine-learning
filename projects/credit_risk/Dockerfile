FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir $(grep -v airflow requirements.txt | sed 's/#.*//')
COPY src ./src
COPY artifacts/champion.joblib ./artifacts/champion.joblib
EXPOSE 8000
CMD ["uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8000"]
