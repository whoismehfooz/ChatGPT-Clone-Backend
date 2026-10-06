FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ui ./ui

EXPOSE 8501

CMD ["streamlit","run","ui/app.py","--server.address=0.0.0.0","--server.port=8501"]
