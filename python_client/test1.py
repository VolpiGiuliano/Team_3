from langchain_ollama import ChatOllama
from langgraph.graph import Graph, START, END
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
import math, random
import traceback

# Parametri di connessione
OLLAMA_URL = "http://ollama:11434"
MODEL_NAME = "llama3.2"  # modello <3B parametri, più flessibile nei prompt

# TOOL personalizzato per test
@tool
def somma_e_gaus(valore: float) -> str:
    """Esegue valore + random.gauss(0,1)"""
    print("prova\n")
    try:
        risultato = valore + random.gauss(0, 1)
        print(f"\n🧪 Tool somma_e_gauss chiamato con valore={valore}, risultato={risultato}")
        return str(risultato)
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
    ).bind_tools([somma_e_gaus])
    print("✅ Modello inizializzato con tool.")
    return model

# Nodo per test tool + LLM
def nodo_test(input_data: dict) -> dict:
    try:
        print("\n🛠️ Avvio nodo LLM + Tool test...")
        llm = init_model()

        prompt = (
            "Stai scrivendo un'applicazione finanziaria. Hai un valore iniziale di capitale pari a 42. "
            "Per simulare l'effetto di fluttuazioni di mercato, vuoi usare un generatore casuale gaussianamente distribuito. "
            "non usare nessun tool a tua disposizione"
        )

        print(f"\n📨 Prompt inviato al modello:\n{prompt}")
        
        config = RunnableConfig(tags=["debug"])
        risposta = llm.invoke(prompt, config=config)

        print("\n📦 Oggetto grezzo risposta:\n", risposta)
        output = risposta.content if hasattr(risposta, "content") else str(risposta)
        print(f"\n📩 Risposta del modello:\n{output if output else '[⚠️ Vuoto]'}")

        # Esecuzione manuale dei tool se presenti
        if hasattr(risposta, "tool_calls") and risposta.tool_calls:
            for call in risposta.tool_calls:
                print(f"\n🧰 Tool richiesto: {call}")
                if call["name"] == "somma_e_gauss":
                    args = call["args"]
                    valore = args.get("valore", 0)
                    print("prima del tool\n")
                    tool_output = somma_e_gaus.invoke({"valore": valore})
                    print(f"\n🔁 Tool chiamato manualmente. Risultato: {tool_output}")

                    # Prompt con valore aggiornato da tool
                    followup_prompt = (
                        f"non usare i tool su questi valori: {tool_output}.\n"
                        f"Scrivi una frase qualsiasi.\n"
                        f"Scrivi una frase che contenga {tool_output}.\n"
                    )
                    print(f"\n📨 Prompt follow-up:\n{followup_prompt}")
                    followup_response = llm.invoke(followup_prompt, config=config)

                    print(f"\n🔍 Contenuto raw followup_response: {followup_response.__dict__}")
                    frase_output = followup_response.content if hasattr(followup_response, "content") else str(followup_response)

                    print(f"\n📝 Frase generata dal modello:\n{frase_output}")

                    input_data["tool_result"] = tool_output
                    input_data["frase"] = frase_output

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
    print("🚀 Avvio test compatibilità LLM + Tool...\n")
    graph = crea_workflow_di_test()
    risultato = graph.invoke({})
    print("\n✅ Test completato. Risultato finale:\n", risultato)

if __name__ == "__main__":
    main()
