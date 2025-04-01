import os           # per il salvataggio nel volume
import requests     # per il controllo dello stato di ollama
from langchain_core.prompts import PromptTemplate   # per l'uso di promt strutturati
from langchain_ollama import OllamaLLM              # integrazione ollama con langchain

OLLAMA_URL = "http://ollama:11434"  # url api di ollama
MODEL_NAME = "llama3"               # nome modello usato

# 1. Verifica se il modello è installato
def model_exists(model_name):
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        response.raise_for_status()
        models = response.json().get("models", [])
        return any(m["name"].startswith(model_name) for m in models)
    except Exception as e:
        print(f"Errore nella verifica del modello: {e}")
        return False

# 2. Installa il modello se non presente
def pull_model(model_name):
    print(f"📥 Scaricamento modello '{model_name}' da Ollama...")
    response = requests.post(f"{OLLAMA_URL}/api/pull", json={"name": model_name}, stream=True)
    for line in response.iter_lines():
        print(line.decode())

# inizializza l'agente
def init_model():
    return OllamaLLM(
        base_url=OLLAMA_URL,
        model=MODEL_NAME
    )

# definisce le regole di generazione
def get_prompt_template():
    return PromptTemplate(
        input_variables=["argomento"],  # definizione di variabile di prompt
        template="Scrivi il seguente documento: {argomento}, tono professionale, lingua italiana."
    )

# definisce la catena di chiamata che deve effettuare l'agente al modello
def run_chain(prompt, llm, input_data):
    chain = prompt | llm
    return chain.invoke(input_data)

# salva l'output in un file txt
def salva_output(text, filename="outputs/output.txt"):
    os.makedirs("outputs", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(text))
    print(f"\n💾 Output salvato in '{filename}'")

def main():
    if not model_exists(MODEL_NAME):
        pull_model(MODEL_NAME)

    llm = init_model()
    prompt = get_prompt_template()
    Argomento = "Estratto conto"    # input manuale che può essere sostituito da un inputs dinamico
    input_data = {"argomento": Argomento}   # sostituisce i l'input alla parola argomento presente nel prompt
    risposta = run_chain(prompt, llm, input_data)
    print("\n🧠 Risposta generata:\n")
    print(risposta)
    salva_output(risposta)

if __name__ == "__main__":
    main()
