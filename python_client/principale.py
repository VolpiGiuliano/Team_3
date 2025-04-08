from langgraph.graph import StateGraph, START, END
from Evento import crea_sottografo_evento
from generazione_dati import crea_sottografo_tabella
import os


def grafo():
    workflow = StateGraph(dict)  # usa uno stato strutturato come dizionario

    tabella_graph = crea_sottografo_tabella()
    evento_graph = crea_sottografo_evento()

    workflow.add_node("Tabella", tabella_graph)
    workflow.add_node("Evento", evento_graph)

    workflow.add_edge(START, "Tabella")
    workflow.add_edge("Tabella", "Evento")
    workflow.add_edge("Evento", END)

    return workflow.compile()


def prompt():
    return "Genera una tabella di 5 colonne di lavori: |impiegato|operaio|imprenditore|disoccupato|pensionato|altro| e 10 righe di spese: |alimentari|alcolici|abbigliamento|abitazione|salute|trasporti|comunicazione|ricreazione|istruzione|assicurazione|poliza"


def salva_output(text, filename="outputs/output.txt"):
    os.makedirs("outputs", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(text))
    print(f"\n💾 Output salvato in '{filename}'")


def main():
    app = grafo()
    stato_iniziale = {"prompt": prompt()}  # input iniziale esplicito per lo stato
    risposta = app.invoke(stato_iniziale)

    print("\n🧠 Risposta generata:")
    print(risposta.get("tabella"))
    print(risposta.get("tabella_modificata"))
    salva_output(risposta.get("tabella_modificata"))


if __name__ == "__main__":
    main()
