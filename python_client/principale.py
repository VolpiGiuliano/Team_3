from langgraph.graph import Graph, START, END
from Evento import crea_sottografo_evento  # importa il sottografo evento
from generazione_dati import crea_sottografo_tabella
from langchain_core.prompts import PromptTemplate   # per l'uso di promt strutturati
import os

def grafo():
    workflow = Graph()

    tabella_graph = crea_sottografo_tabella()
    evento_graph = crea_sottografo_evento()
    
    workflow.add_node("Evento", evento_graph)
    workflow.add_node("Tabella", tabella_graph)
    #workflow.add_node("verifica", nodo_verifica)

    workflow.add_edge(START, "Tabella")
    workflow.add_edge("Tabella", "Evento")
    workflow.add_edge("Evento", END)
    
    return workflow.compile()

def prompt():
    return "Genera una tabella di 5 colonne di lavori: |impiegato|operaio|imprenditore|disoccupato|pensionato| e 10 righe di spese: |alimentari|alcolici|abbigliamento|abitazione|salute|trasporti|comunicazione|ricreazione|istruzione|assicurazione|poliza"

# salva l'output in un file txt
def salva_output(text, filename="outputs/output.txt"):
    os.makedirs("outputs", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(text))
    print(f"\n💾 Output salvato in '{filename}'")

def main():
    app = grafo()

    risposta = app.invoke(prompt())

    print("\n🧠 Risposta generata:\n")
    print(risposta["tabella"])
    print(risposta["tabella_modificata"])
    salva_output(risposta["tabella_modificata"])

if __name__ == "__main__":
    main()