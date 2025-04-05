import os           # per il salvataggio nel volume
import requests     # per il controllo dello stato di ollama
import numpy as np
import pandas as pd
from langchain_ollama import OllamaLLM              # integrazione ollama con langchain
from langgraph.graph import Graph, START, END

OLLAMA_URL = "http://ollama:11434"  # url api di ollama
MODEL_NAME = "llama3.2"               # nome modello usato

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
    #print(df)
    return {"tabella": df}  # <-- passa come dizionario per il sottografo evento


def crea_sottografo_tabella():

    tabella_graph = Graph()

    tabella_graph.add_node("ollama", ollama)
    tabella_graph.add_node("constraints", constraints)

    tabella_graph.add_edge(START, "ollama")
    tabella_graph.add_edge("ollama", "constraints")
    tabella_graph.add_edge("constraints", END)

    return tabella_graph.compile()