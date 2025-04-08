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
avgJob = [[3357.79, 0.8],[2513.93, 1.1],[4139.97, 2.5],[1920.94, 2.5],[2498.17, 1.0]]
avgSpe = [[460.72, 2.81],[41.85, 0.45],[109.14, 1.84],[693.39, 5.53],[87.41, 1.69],[335.94, 5.65],[44.32, 0.38],[94.08, 1.49],[27.02, 1.24],[83.85, 3.69]]
sum = np.sum(avgSpe, axis=0)[0]

# inizializza l'agente
def init_model():
    return OllamaLLM(
        base_url=OLLAMA_URL,
        model=MODEL_NAME
    )

# definisce la catena di chiamata che deve effettuare l'agente al modello
def ollama(input_data):
    llm = init_model()
    return llm.invoke(prompt())

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
                    table[k][l] = np.random.normal(loc=(float(num) + (avgJob[l][0]*avgSpe[k][0]/sum))/2, scale=avgJob[l][1]+avgSpe[k][1])
                l+=1
                hasEl = True
            except ValueError: 
                pass
        if hasEl == True:
            k+=1
    return table

def check(input_data):
    if np.any(input_data):
        return "results"
    else:
        print("Errore, richiamo")
        return "ollama"

def results(input_data):
    df = pd.DataFrame(table, columns=["Impiegato", "Operaio", "Imprenditore", "Disoccupato", "Pensionato"])
    df.index = ["Alimentari","Alcolici","Abbigliamento","Abitazione","Salute","Trasporti","Comunicazione","Ricreazione","Istruzione","Assicurazione"]
    return df

def prompt():
    return "Genera una tabella di 5 colonne di lavori: |impiegato|operaio|imprenditore|disoccupato|pensionato|altro| e 10 righe di spese: |alimentari|alcolici|abbigliamento|abitazione|salute|trasporti|comunicazione|ricreazione|istruzione|assicurazione|poliza"

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
    workflow.add_node("results", results)

    workflow.add_edge(START, "ollama")
    workflow.add_edge("ollama", "constraints")
    workflow.add_conditional_edges("constraints", check)
    workflow.add_edge("results", END)

    app = workflow.compile()

    risposta = app.invoke(prompt())

    print("\n🧠 Risposta generata:\n")
    print(risposta)
    salva_output(risposta)

if __name__ == "__main__":
    main()
