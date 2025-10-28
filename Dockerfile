FROM python:3.11-slim

WORKDIR /app
COPY . /app

# Install dependencies
RUN apt-get update -y && apt-get install -y --no-install-recommends awscli \
 && pip install --no-cache-dir -r requirements.txt \
 && chmod +x start.sh

# Expose ports for API and Streamlit
EXPOSE 8000 8501

# Run both processes via script
CMD ["./start.sh"]