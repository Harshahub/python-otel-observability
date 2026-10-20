FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file and install Flask
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your main.py file
COPY main.py .

EXPOSE 5000

CMD ["python", "main.py"]
