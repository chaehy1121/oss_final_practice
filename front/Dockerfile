FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8501

ENV FASTAPI_HOST=98.94.222.157

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
