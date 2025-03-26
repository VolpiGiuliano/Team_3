import requests

# Imposta nome del modello (es. llama2, mistral, ecc.)
MODEL_NAME = "llama2"
OLLAMA_URL = "http://ollama:11434"

# Funzione per verificare se il modello è disponibile
def model_exists(model_name):
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")   # chiama l'api di ollama
        if response.status_code == 200:                     #controlla che l'api risponda
            models = response.json().get("models", [])
            return any(m["name"].startswith(model_name) for m in models) # controlla che il modello installato sia lo stesso di quello richiesto
        else:
            print(f"Errore nella richiesta: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:     # errore nell'url, nella rete o docker ollama spento
        print("⚠️ Impossibile connettersi a Ollama. È in esecuzione?")
        return False

# Funzione per generare una risposta
def generate_response(prompt):
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False     # la risposta non viene divisa in più parti
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=data) # invia il prompt all'api
    return response.json()["response"]

# --- Programma principale ---
if model_exists(MODEL_NAME):
    prompt = input("Scrivi il tuo prompt per il modello: ") # interrattività per inserire il prompt
    risposta = generate_response(prompt)
    print("🧠 Risposta del modello:", risposta)
else:
    print(f"❌ Il modello '{MODEL_NAME}' non è disponibile su Ollama.")
    print(f"Puoi scaricarlo con:\n  ollama pull {MODEL_NAME}")  # comando da usare nel terminale di ollama