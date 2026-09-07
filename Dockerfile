FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# 0.0.0.0 is required so the API is accessible outside the Docker container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]