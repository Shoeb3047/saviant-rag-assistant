FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir uv

# Copy only necessary files
COPY requirements.txt ./
RUN uv pip install --system -r requirements.txt && pip cache purge

COPY main.py .
COPY rag_service ./rag_service

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
