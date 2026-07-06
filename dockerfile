FROM python:3.11-slim

# Bonnes pratiques : pas de .pyc, logs non bufferises
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# On copie d'abord les dependances : le cache Docker n'est invalide
# que si requirements.txt change (rebuild plus rapide).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Puis le code applicatif
COPY . .

# Securite : on ne tourne pas en root
RUN useradd -m appuser
USER appuser

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
