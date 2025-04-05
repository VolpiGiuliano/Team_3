from langgraph.graph import Graph, START, END
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
import os
import math
import random

OLLAMA_URL = "http://ollama:11434"
MODEL_NAME = "llama3.2"
MAX_TENTATIVI = 3
MAX_GENERAZIONI = 1

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

def nodo_evento(input_data):
    input_data["evento"] = "crisi economica globale"
    return input_data

def nodo_modifica(input_data):
    if isinstance(input_data, tuple):
        _, input_data = input_data

    input_data["tentativi"] = input_data.get("tentativi", 0) + 1
    llm = init_model()
    df = input_data["tabella"]
    evento = input_data["evento"]

    prompt = (
        f"Ecco una tabella di spese in base alle professioni:\n\n{df}\n\n"
        f"In seguito all'evento: {evento}, decidi che modifiche fare.\n"
        f"Per ogni modifica matematica usa il tool calcola_probabilita.\n"
        f"Esempio: calcola_probabilita(expr='valore * 0.8', valore=3200)"
    )

    config = RunnableConfig()
    output = llm.invoke(prompt, config=config)
    response = output.content if hasattr(output, "content") else str(output)

    input_data["tabella_modificata"] = df
    return input_data

def nodo_verifica(input_data):
    if input_data.get("tentativi", 0) >= MAX_TENTATIVI:
        input_data["verifica"] = "ok (forzato dopo limite tentativi)"
        return "ok", input_data
    llm = init_model()
    prompt = f"Controlla la coerenza della seguente tabella modificata. Rispondi con 'ok' o 'errore':\n{input_data['tabella_modificata']}"
    esito_raw = llm.invoke(prompt)
    esito = esito_raw.content.strip().lower() if hasattr(esito_raw, "content") else str(esito_raw).strip().lower()
    input_data["verifica"] = esito
    return ("ok" if "ok" in esito else "errore"), input_data

def crea_sottografo_evento():
    evento_graph = Graph()
    evento_graph.add_node("evento", nodo_evento)
    evento_graph.add_node("modifica", nodo_modifica)
    evento_graph.add_node("verifica", nodo_verifica)
    
    evento_graph.add_edge(START, "evento")
    evento_graph.add_edge("evento", "modifica")
    evento_graph.add_edge("modifica", END)
    #evento_graph.add_conditional_edges("verifica", lambda result: result[0], {"ok": END, "errore": "modifica"})
    return evento_graph.compile()
