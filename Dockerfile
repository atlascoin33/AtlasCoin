FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || echo "No requirements.txt"

EXPOSE 8000

CMD ["python3", "node.py"]
