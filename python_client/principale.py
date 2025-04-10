from langgraph.graph import StateGraph, START, END
from Evento import crea_sottografo_evento
from generazione_dati import crea_sottografo_tabella
import os
import requests

OLLAMA_URL = "http://ollama:11434"  # url api di ollama
MODEL_NAME_1 = "llama3"
MODEL_NAME_2 = "llama3.2"

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

def grafo():
    workflow = StateGraph(dict)  # usa uno stato strutturato come dizionario

    tabella_graph = crea_sottografo_tabella()
    evento_graph = crea_sottografo_evento()

    workflow.add_node("Tabella", tabella_graph)
    workflow.add_node("Evento", evento_graph)
    workflow.add_node("Salva_Tabella", salva_output)

    workflow.add_edge(START, "Tabella")
    workflow.add_edge("Tabella", "Salva_Tabella")
    workflow.add_conditional_edges("Salva_Tabella", check)
    #workflow.add_edge("Evento", END)

    return workflow.compile()


def prompt():
    return "Genera una tabella di 5 colonne di lavori: |impiegato|operaio|imprenditore|disoccupato|pensionato|altro| e 10 righe di spese: |alimentari|alcolici|abbigliamento|abitazione|salute|trasporti|comunicazione|ricreazione|istruzione|assicurazione|poliza"

def evento():
    return "crisi climatica globale"

def numero_generazioni():
    return "72"

def salva_output(state: dict) -> dict:
    filename=f"outputs/output.txt"
    os.makedirs("outputs", exist_ok=True)
    with open(filename, 'a', encoding="utf-8") as f:
        f.write(str(state.get("tabella")) + "\n\n")
    #print(f"\n💾 Output salvato in '{filename}'")

def check(state: dict) -> dict:
    N_gerazioni_Max = int(state.get("N_gen"))
    i = int(state.get("N_gen_i"))

    if N_gerazioni_Max > i:
        i = i + 1
        state["N_gen_i"] = str(i)
        return "Tabella"
    else:
        return "END"
        #return "Evento"

def main():

    if not model_exists(MODEL_NAME_1):
        pull_model(MODEL_NAME_1)

    if not model_exists(MODEL_NAME_2):
        pull_model(MODEL_NAME_2)

    app = grafo()
    stato_iniziale = {"prompt": prompt(), "evento": evento(), "N_gen": numero_generazioni(), "N_gen_i": "1"}  # input iniziale esplicito per lo stato
    risposta = app.invoke((stato_iniziale), {"recursion_limit": 100})

    #print("\n🧠 Risposta generata:")
    #print(risposta.get("tabella"))
    #print(risposta.get("tabella_modificata"))


if __name__ == "__main__":
    main()
