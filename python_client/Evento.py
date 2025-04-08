from langgraph.graph import Graph, START, END
from langchain_ollama import ChatOllama
from langchain.tools import tool
import os
import math
import random

# Configurazione modello
OLLAMA_URL = "http://ollama:11434"
MODEL_NAME = "llama3.2"

MAX_TENTATIVI = 3
MAX_GENERAZIONI = 1

# TOOL: Calcola un'espressione matematica/probabilistica usando 'valore'
@tool
def calcola_probabilita(expr: str, valore: float) -> str:
    """
    Valuta un'espressione matematica che usa la variabile 'valore'.
    Esempi: 'valore * 0.75', 'valore + random.gauss(-200, 50)'
    Funzioni disponibili: math.*, random.*
    """
    try:
        safe_globals = {
            "__builtins__": {},
            "math": math,
            "random": random,
            "valore": valore
        }
        result = eval(expr, safe_globals, {})
        return str(result)
    except Exception as e:
        return f"Errore nel calcolo: {e}"

def init_model():
    return ChatOllama(model=MODEL_NAME, base_url=OLLAMA_URL).bind_tools([calcola_probabilita])

# Nodo 1: Inserimento evento
def nodo_evento(input_data):
    input_data["evento"] = "crisi economica globale"
    return input_data

# Nodo 2: Modifica tabella in base all'evento
def nodo_modifica(input_data):
    if isinstance(input_data, tuple):
        _, input_data = input_data  # scarta "ok"/"errore", tieni il dizionario

    input_data["tentativi"] = input_data.get("tentativi", 0) + 1
    llm = init_model()
    tabella = input_data["tabella"]
    evento = input_data["evento"]
    prompt = (
        f"Dati questi dati in formato tabellare: \n{tabella}\n\n"
        f"E questo evento: '{evento}'\n\n"
        f"Per ogni cella da modificare per cui servono dei calcoli usa il tool disponibile\n"
    )
    output = llm.invoke(prompt)
    response = output.content if hasattr(output, "content") else str(output)
    input_data["tabella_modificata"] = response
    return input_data

# Nodo 3: Verifica coerenza (condizionale)
def nodo_verifica(input_data):
    if input_data.get("tentativi", 0) >= MAX_TENTATIVI:
        input_data["verifica"] = "ok (forzato dopo limite tentativi: errore di coerenza ingestibile)"
        return "ok", input_data

    llm = init_model()
    tabella_modificata = input_data["tabella_modificata"]
    prompt = f"Controlla la coerenza della seguente tabella modificata. Rispondi solo con 'ok' oppure 'errore':\n{tabella_modificata}"
    esito_raw = llm.invoke(prompt)
    esito = esito_raw.content.strip().lower() if hasattr(esito_raw, "content") else str(esito_raw).strip().lower()
    input_data["verifica"] = esito
    return ("ok" if "ok" in esito else "errore"), input_data

# Creazione del sottografo evento con loop su verifica
def crea_sottografo_evento():
    evento_graph = Graph()
    evento_graph.add_node("evento", nodo_evento)
    evento_graph.add_node("modifica", nodo_modifica)
    evento_graph.add_node("verifica", nodo_verifica)

    evento_graph.add_edge(START, "evento")
    evento_graph.add_edge("evento", "modifica")
    evento_graph.add_edge("modifica", "verifica")
    evento_graph.add_conditional_edges(
        "verifica",
        lambda result: result[0],
        {
            "ok": END,
            "errore": "modifica"
        }
    )

    return evento_graph.compile()

# ESEMPIO DI USO ISOLATO
if __name__ == "__main__":
    sottografo = crea_sottografo_evento()
    os.makedirs("outputs/debug_output", exist_ok=True)

    for i in range(1, (MAX_GENERAZIONI+1)):
        print(f"\n🔧 Generazione tabella iniziale per input_data {i}:")
        llm = init_model()
        prompt_tabella = "Genera una tabella di 4 colonne nel seguente formato: |sesso|età|lavoro|entrate mensili|"
        grezzo = llm.invoke(prompt_tabella)
        tabella_generata = "\n".join(
            [riga for riga in grezzo.content.splitlines() if riga.strip().startswith("|")]
            if hasattr(grezzo, "content") else
            [riga for riga in str(grezzo).splitlines() if riga.strip().startswith("|")]
        )

        print(tabella_generata)

        input_dati = {
            "tabella": tabella_generata
        }

        risultato = sottografo.invoke(input_dati)

        if isinstance(risultato, tuple):
            _, risultato = risultato

        with open(f"outputs/debug_output/output_debug_{i}.txt", "w", encoding="utf-8") as f:
            f.write("# Debug Output del sottografo evento\n\n")
            f.write(f"evento:\n{risultato.get('evento', '')}\n\n")
            f.write(f"tabella_modificata:\n{risultato.get('tabella_modificata', '')}\n")

        with open(f"outputs/debug_output/tabella_generata_{i}.txt", "w", encoding="utf-8") as f:
            f.write(tabella_generata)
