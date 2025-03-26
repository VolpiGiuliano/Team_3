# Usa un'immagine base di Python
FROM python:3.9

# Imposta la directory di lavoro
WORKDIR /ollama-api

# Copia il file requirements.txt e installa le dipendenze
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia il codice dell'applicazione
COPY . .

# Comando per avviare l'applicazione
CMD ["python", "ollama_api.py"]