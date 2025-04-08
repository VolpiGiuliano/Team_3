# Progetto Team 3

## Idea Dati Sintetici
**Finalità del modello:** generare dati sintetici relativi alle spese per consumi degli individui.

Sfruttando dati aggregati e pubblicamente disponibili (ISTAT) si vuole creare un modello in grado di simulare le spese mensili (o annuali) aggregate sostenute dagli individui all’interno del territorio nazionale. La spesa per consumi viene articolata nel seguente modo:

### **Voci di spesa**
- **Prodotti alimentari**

- **Prodotti non alimentari e servizi**
  - Alcolici
  - Abbigliamento
  - Abitazione
  - Salute
  - Trasporti
  - Comunicazione
  - Ricreazione
  - Istruzione
  - Assicurazione

### **Condizione professionale**
- **Occupato**
  - Dipendente
    - Impiegato
    - Operaio

- **Non occupato**
  - Disoccupato
  - Pensionato


Il formato finale si presenterà come un file TXT con all'interno i dati in formato tabulare con ogni voce sopra descritta come singola colonna e le osservazioni (i soggetti) saranno divisi in singole righe. 

![Output](grafi/output.png)
---
## Descrizione Contenuto
- Docker presenti
    - docker python
    - docker ollama
- Docker-compose: crea la rete condivisa per poter far parlare i docker tra di loro localmente
- Dockerfile dello script python: crea l'immagine del docker per far girare lo script python
- Script python: comunica con l'api di ollama per sfruttare il modello installato

---

## Descrizione funzinamento grafo

**Finalità della decisione**:
Il grafo decisionale serve come base per la definizione del loop decisionale langgraph che dovrà compiere l'agente manager. Esso dovrà comprendere l'input manuale, effettuerà un controllo di adeguatezza dei risultati e valuterà se sarà necessario rifare da capo la generazione o mostrare i risultati ottenuti e definire di quali dati il tool avrà bisogno. Successivamente aggregherà i risultati e genererà la risposta iniziale. 

![Grafo decisionale](grafi/Grafo%20decisionale.png)
