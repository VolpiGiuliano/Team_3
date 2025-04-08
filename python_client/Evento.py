from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
import pandas as pd

OLLAMA_URL = "http://ollama:11434"
MODEL_NAME = "llama3.2"

# Funzione di utilità normale, non decorata come tool

def nodo_evento(state: dict) -> dict:
    state["evento"] = "crisi economica globale"
    return state



def moltiplica_per_valore(df: dict, moltiplicatore: float) -> dict:
    """
    calcola le percentuali.
    """
    try:
        df = pd.DataFrame(df)
        df = df * moltiplicatore
        return df.to_dict()
    except Exception as e:
        return {"errore": str(e)}

# Modello con tool binding (non serve tool in questa fase)
def init_model():
    return ChatOllama(
        model=MODEL_NAME,
        base_url=OLLAMA_URL,
    )

# Nodo in cui il modello decide il moltiplicatore da passare al tool
def nodo_decisione_llm(state: dict) -> dict:
    llm = init_model()
    df = state.get("tabella")
    if isinstance(df, pd.DataFrame):
        df_str = df.to_string()
    else:
        df_str = str(df)

    prompt = (
        f"in base a questo {state['evento']} definisci la variazione delle seguenti categorie di spesa mensile: alimentari,alcolici,abbigliamento,abitazione,salute,trasporti,comunicazione,ricreazione,istruzione,assicurazione"
        f"scrivi solo la variazione percentuale"
    )

    output = llm.invoke(prompt)
    try:
        moltiplicatore = float(output.content.strip())
        state["moltiplicatore"] = moltiplicatore
    except:
        state["errore"] = f"Impossibile interpretare risposta LLM: {output.content}"
    return state

# Nodo che applica la trasformazione direttamente
def applica_tool_senza_llm(state: dict) -> dict:
    moltiplicatore = state.get("moltiplicatore")
    tabella = state.get("tabella")

    if isinstance(tabella, pd.DataFrame):
        df_dict = tabella.to_dict()
    else:
        df_dict = tabella

    risultato = moltiplica_per_valore(df=df_dict, moltiplicatore=moltiplicatore)
    try:
        df = pd.DataFrame(risultato)
        state["tabella"] = df
        print("\n🔄 Tabella aggiornata con moltiplicatore applicato:\n", df)
    except Exception as e:
        state["errore"] = str(e)

    return state

# Sottografo
def crea_sottografo_evento():
    grafo = StateGraph(dict)
    grafo.add_node("evento", nodo_evento)
    grafo.add_node("scegli_moltiplicatore", nodo_decisione_llm)
    grafo.add_node("applica_tool", applica_tool_senza_llm)

    grafo.add_edge(START, "evento")
    grafo.add_edge("evento", "scegli_moltiplicatore")
    grafo.add_edge("scegli_moltiplicatore", "applica_tool")
    grafo.add_edge("applica_tool", END)

    return grafo.compile()
