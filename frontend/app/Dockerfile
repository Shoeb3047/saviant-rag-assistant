# frontend/app/Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install pip and only required deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend code
COPY streamlit_app.py .

EXPOSE 8501

# CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"] <-- Earlier 
# CMD ["streamlit", "run", "streamlit_app.py", "--server.port=$PORT", "--server.address=0.0.0.0"]   <-- Earlier 
CMD ["sh", "-c", "streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0"]





