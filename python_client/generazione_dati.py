import requests

# Imposta nome del modello (es. llama2, mistral, ecc.)
MODEL_NAME = "llama3"
OLLAMA_URL = "http://ollama:11434"

""" Funzione per verificare se il modello è disponibile.
    Se il collegamento con ollama fallisce la funzione 
    stampa l'errore e restituisce False
"""
def model_exists(model_name):
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")   # chiama l'api di ollama
        if response.status_code == 200:                     # controlla che l'api risponde
            models = response.json().get("models", [])
            return any(m["name"].startswith(model_name) for m in models) #controlla che il modello richiesto sia presente
        else:
            print(f"Errore nella richiesta: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:             # errore di connessione al docker ollama
        print("⚠️ Impossibile connettersi a Ollama. È in esecuzione?")
        return False

# Prompt per generazione condizionale
def generate_prompt():
    # definisce il parametro di contesto per la generazione condizionale
    context = """
    ### CONTEXT:
    Azienda: ABC Corp
    Settore: Finanza
    Trimestre: Q3 2024
    Risultati: Ricavi 145M€, utile netto 22M€, crescita 6%, debito ridotto del 3% rispetto al Q2

    ### INSTRUCTION:
    Scrivi un report finanziario realistico e coerente basato sul contesto fornito.
    """

    # Payload per la richiesta
    payload = {
        "model": MODEL_NAME,
        "prompt": context,
        "options": {
            "temperature": 0.8,     # definisce la creatività: 0.1 poco creativo
            "top_p": 0.95,          # definisce i token per la generazione
            "num_predict": 300,     # numero di token da generare: definiscono la lunghezza del documento
            "repeat_penalty": 1.2   # evita le ripetizioni di parole nei documenti
        },
        "stream": False             # la risposta è in un unico prompt
    }

    # Chiamata HTTP verso l'API di Ollama
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload) # sfrutta l'api per mandare la richiesta
     
    # controllo di richiesta andata a buon fine
    if response.ok:
        return response.json()["response"]
    else:
        print("❌ Errore:", response.status_code, response.text)

# Output
if model_exists(MODEL_NAME):
    result = generate_prompt()
    print("\n--- OUTPUT ---\n")
    print("🧠 Risposta del modello:", result)
else:
    print(f"❌ Il modello '{MODEL_NAME}' non è disponibile su Ollama.")
    print(f"Puoi scaricarlo con:\n  ollama pull {MODEL_NAME}")
