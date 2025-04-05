import os           # per il salvataggio nel volume
import requests     # per il controllo dello stato di ollama
import numpy as np
import pandas as pd
from langchain_core.prompts import PromptTemplate   # per l'uso di promt strutturati
from langchain_ollama import OllamaLLM              # integrazione ollama con langchain
from langgraph.graph import Graph, START, END

OLLAMA_URL = "http://ollama:11434"  # url api di ollama
MODEL_NAME = "llama3"               # nome modello usato

table = np.zeros((10,5))
v = []

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

def evento(input_data):
    llm = init_model()
    data = input_data.split("\n\n")
    return llm.invoke(f"Quale di questi valori si modificherà se succede questo {input}")

def constraints(input_data):
    data = input_data.split("\n\n")
    data = data[1].split("\n")
    k=0
    for i in range(len(data)):
        line = data[i].split("|")
        hasEl = False
        l=0
        for j in range(len(line)):
            try:
                if l<5 and k<10:
                    num=line[j].strip()
                    num = num.replace("€", "")
                    table[k][l] = float(num)
                l+=1
                hasEl = True
            except ValueError: 
                pass
        if hasEl == True:
            k+=1
    df = pd.DataFrame(table, columns=["Impiegato", "Operaio", "Imprenditore", "Disoccupato", "Pensionato"])
    df.index = ["Alimentari","Alcolici","Abbigliamento","Abitazione","Salute","Trasporti","Comunicazione","Ricreazione","Istruzione","Assicurazione"]
    print(df)
    return df

def prompt():
    return "Genera una tabella di 5 colonne di lavori: |impiegato|operaio|imprenditore|disoccupato|pensionato| e 10 righe di spese: |alimentari|alcolici|abbigliamento|abitazione|salute|trasporti|comunicazione|ricreazione|istruzione|assicurazione|poliza"

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
