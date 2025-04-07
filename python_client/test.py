from langchain_ollama import ChatOllama
from langgraph.graph import Graph, START, END
from langchain_core.runnables import RunnableConfig, RunnableLambda
from langchain.tools import tool
import math, random
import traceback

# Parametri di connessione
OLLAMA_URL = "http://ollama:11434"
MODEL_NAME = "mistral"  # modello <3B parametri, più flessibile nei prompt

# TOOL personalizzato per test
@tool
def somma_e_gauss(valore: float) -> str:
    """Esegue valore + random.gauss(0,1)"""
    try:
        risultato = valore + random.gauss(0, 1)
        print(f"\n🧪 Tool somma_e_gauss chiamato con valore={valore}, risultato={risultato}")
        return (risultato)
    except Exception as e:
        print(f"\n❌ Errore nel tool somma_e_gauss: {e}")
        traceback.print_exc()
        return f"Errore: {e}"

# Inizializza modello con tool
def init_model():
    print("\n🔌 Inizializzo ChatOllama...")
    model = ChatOllama(
        model=MODEL_NAME,
        base_url=OLLAMA_URL
    ).bind_tools([somma_e_gauss])
    print("✅ Modello inizializzato con tool.")
    return model

# Nodo per test tool + LLM
def nodo_test(input_data: dict) -> dict:
    try:
        print("\n🛠️ Avvio nodo LLM + Tool test...")
        llm = init_model()

        prompt = (
            f"Devi applicare il tool `somma_e_gauss` a questo numero: 42.\n "
            f"Scrivi una frase che contnga il risultato della chiamata del tool"
        )

        print(f"\n📨 Prompt inviato al modello:\n{prompt}")

        config = RunnableConfig(tags=["debug"])

        # Esecuzione stile LangChain con tool handler incluso
        pipeline = llm | RunnableLambda(lambda x: x)
        risposta = pipeline.invoke(prompt, config=config)

        print("\n📦 Oggetto grezzo risposta:\n", risposta)
        output = risposta.content if hasattr(risposta, "content") else str(risposta)
        print(f"\n📩 Risposta del modello:\n{output if output else '[⚠️ Vuoto]'}")

        input_data["risposta"] = output
        return input_data
    except Exception as e:
        print(f"\n❌ Errore durante l'esecuzione del nodo_test: {e}")
        traceback.print_exc()
        input_data["errore"] = str(e)
        return input_data

# Costruzione grafo LangGraph
def crea_workflow_di_test():
    print("\n🧱 Creo il workflow di test...")
    g = Graph()
    g.add_node("test", nodo_test)
    g.add_edge(START, "test")
    g.add_edge("test", END)
    return g.compile()

# Funzione main
def main():
    print("\n🚀 Avvio test compatibilità LLM + Tool...\n")
    graph = crea_workflow_di_test()
    risultato = graph.invoke({})
    print("\n✅ Test completato. Risultato finale:\n", risultato)

if __name__ == "__main__":
    main()
