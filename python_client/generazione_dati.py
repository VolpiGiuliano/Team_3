import os           # per il salvataggio nel volume
import requests     # per il controllo dello stato di ollama
from langchain_core.prompts import PromptTemplate   # per l'uso di promt strutturati
from langchain_ollama import OllamaLLM              # integrazione ollama con langchain
from langgraph.graph import Graph, START, END

OLLAMA_URL = "http://ollama:11434"  # url api di ollama
MODEL_NAME = "llama3"               # nome modello usato

# inizializza l'agente
def init_model():
    return OllamaLLM(
        base_url=OLLAMA_URL,
        model=MODEL_NAME
    )

# definisce la catena di chiamata che deve effettuare l'agente al modello
def ollama(input_data):
    llm = init_model()
    return llm.invoke(input_data)

def constraints(input_data):
    data = input_data.split("\n\n")
    return data[1]

def prompt():
    return "Genera una tabella di 4 colonne nel seguente formato: |sesso|età|lavoro|entrate mensili|"

# salva l'output in un file txt
def salva_output(text, filename="outputs/output.txt"):
    os.makedirs("outputs", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(text))
    print(f"\n💾 Output salvato in '{filename}'")

def main():

    workflow = Graph()

    workflow.add_node("ollama", ollama)
    workflow.add_node("constraints", constraints)

    workflow.add_edge(START, "ollama")
    workflow.add_edge("ollama", "constraints")
    workflow.add_edge("constraints", END)

    app = workflow.compile()

    risposta = app.invoke(prompt())

    print("\n🧠 Risposta generata:\n")
    print(risposta)
    salva_output(risposta)

if __name__ == "__main__":
    main()
