import requests

# Imposta nome del modello (es. llama2, mistral, ecc.)
MODEL_NAME = "llama2"
OLLAMA_URL = "http://ollama:11434"

# Funzione per verificare se il modello è disponibile
def model_exists(model_name):
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(m["name"].startswith(model_name) for m in models)
        else:
            print(f"Errore nella richiesta: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("⚠️ Impossibile connettersi a Ollama. È in esecuzione?")
        return False

# Funzione per generare una risposta
def generate_response(prompt):
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=data)
    return response.json()["response"]

# --- Programma principale ---
if model_exists(MODEL_NAME):
    prompt = input("Scrivi il tuo prompt per il modello: ")
    risposta = generate_response(prompt)
    print("🧠 Risposta del modello:", risposta)
else:
    print(f"❌ Il modello '{MODEL_NAME}' non è disponibile su Ollama.")
    print(f"Puoi scaricarlo con:\n  ollama pull {MODEL_NAME}")
