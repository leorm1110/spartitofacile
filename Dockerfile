FROM python:3.11-slim

# Installa LibreOffice, pandoc e dipendenze
RUN apt-get update && apt-get install -y libreoffice pandoc && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000
CMD ["python", "converter.py"] 