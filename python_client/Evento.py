from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
import pandas as pd

OLLAMA_URL = "http://ollama:11434"
MODEL_NAME = "llama3.2"

# Funzione di utilità normale, non decorata come tool

def nodo_evento(state: dict) -> dict:
    state["evento"] = "guerra in ucraina"
    return state



def moltiplica_per_valore(df: dict, percentuale) -> dict:
    """
    calcola le percentuali.
    """
    try:
        df = pd.DataFrame(df)
        for i in range(10):
            for j in range(5):
                df.iat[i, j] += df.iat[i, j] * percentuale[i]/100
        return df.to_dict()
    except Exception as e:
        return {"errore": str(e)}

# Modello con tool binding (non serve tool in questa fase)
def init_model():
    return ChatOllama(
        model=MODEL_NAME,
        base_url=OLLAMA_URL,
        config={"system_message": "non generare testo"}
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
        f"In base a questo {state['evento']} genera delle ipotetiche variazioni percentuali delle seguenti categorie di spesa mensile: alimentari,alcolici,abbigliamento,abitazione,salute,trasporti,comunicazione,ricreazione,istruzione,assicurazione"
        f"Scrivi solo le variazioni percentuali separate da virgole, nello stesso ordine"
        f"usa come formato esempio: '-5%, -2%, -10%, 0%, 3%, -7%, 1%, -4%, 2%, -1%'."
        f"non generare testo."
    )

    output = llm.invoke(prompt)
    try:
        contenuto = output.content.strip()
        
        percentuali = [float(x.strip().replace("%", "")) for x in contenuto.split(",")]
        state["percentuali"] = percentuali
    except:
        state["errore"] = f"Impossibile interpretare risposta LLM: {output.content}"
    return state

# Nodo che applica la trasformazione direttamente
def applica_tool_senza_llm(state: dict) -> dict:
    percentuali = state.get("percentuali")
    tabella = state.get("tabella")

    if isinstance(tabella, pd.DataFrame):
        df_dict = tabella.to_dict()
    else:
        df_dict = tabella

    risultato = moltiplica_per_valore(df_dict, percentuali)
    try:
        df = pd.DataFrame(risultato)
        state["tabella_modificata"] = df
        #print("\n🔄 Tabella aggiornata con moltiplicatore applicato:\n", df)
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
