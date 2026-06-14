FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8501

# 컨테이너 환경에서는 FASTAPI_URL 환경변수로 백엔드 주소를 주입받음
# 미설정 시 localhost:8000 으로 동작 (로컬 개발용)
ENV FASTAPI_HOST=localhost

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
