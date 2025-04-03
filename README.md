# Progetto Team 3

## Idea Dati Sintetici
**Finalità del modello:** generare dati sintetici relativi alle spese per consumi degli individui.

Sfruttando dati aggregati e pubblicamente disponibili (ISTAT) si vuole creare un modello in grado di simulare le spese mensili (o annuali) aggregate sostenute dagli individui all’interno del territorio nazionale. La spesa per consumi viene articolata nel seguente modo:

- Spesa per prodotti alimentari e bevande analcoliche
    - Cereali e prodotti a base di cereali
    - Animali vivi, carne e altre parti di animali di terra macellati 
    - Pesci e altri frutti di mare 
    - Latte, altri prodotti lattiero-caseari e uova 
    - Oli e grassi 
    - Frutta e frutta a guscio 
    - Ortaggi, tuberi, platani, banane da cuocere e legumi 
    - Zucchero, prodotti dolciari e dessert 
    - Cibi pronti e altri prodotti alimentari pronti n.a.c. 
    - Succhi di frutta e verdura 
    - Caffè e succedanei del caffè 
    - Tè, mate e altri prodotti vegetali da infusione 
    - Bevande al cacao 
    - Acqua 
    - Bibite 
    - Altre bevande analcoliche 
    - Servizi per la trasformazione delle materie prime in prodotti alimentari e bevande analcoliche
- Spesa per prodotti/servizi non alimentari:
    - Bevande alcoliche e tabacchi;
    - Abbigliamento e calzature;
    - Abitazione, acqua, elettricità, gas e altri combustibili, di cui:
        - Interventi di ristrutturazione
        - Affitti figurativi
    - Mobili, articoli e servizi per la casa
    - alute
    - Trasporti
    - Informazione e comunicazione
    - Ricreazione, sport e cultura
    - Istruzione
    - Servizi di ristorazione e di alloggio
    - Servizi assicurativi e finanziari
    - Beni e servizi per la cura della persona, servizi di protezione sociale e altri beni e servizi
    - 
Le seguenti voci sono dedicate al soggetto delle spese, l'individuo in questione:
- Età
- Sesso
- Regione di residenza
- Tipologia familiare (persone sole, coppie, coppie con figli)
-  Condizione professionale

Il formato finale si presenterà come un file TXT con all'interno i dati in formato tabulare con ogni voce sopra descritta come singola colonna e le osservazioni (i soggetti) saranno divisi in singole righe. 

---
## Descrizione Contenuto
- Docker presenti
    - docker python
    - docker ollama
- Docker-compose: crea la rete condivisa per poter far parlare i docker tra di loro localmente
- Dockerfile dello script python: crea l'immagine del docker per far girare lo script python
- Script python: comunica con l'api di ollama per sfruttare il modello installato


## Descrizione funzinamento grafi
**Finalità della struttra**:
Abbiamo pensato a una struttura gerarchica multi-agente con un agente managere gestisce la comprensione, l'elaborazione e il controllo della generazione, gli agenti subordinati servo principalmente per delegare le chiamate ai tool che non richiedono l'uso di un modello e nel caso sia necessario questa struttura permette l'utilizzo di un modello di prestazioni più ristretto e preciso che non inficia troppo sulle prestazione e garantisce comunque il parallelismo per non perdere velocità di elaborazione.

**Finalità della decisione**:
Il grafo decisionale è ciò che usaremo come base per la definizione del loop decisionale langgraph che dovrà compiere l'agente manager. Esso dovrà comprendere l'input manuale e definire di quali tool avrà bisogno e potrà accedere ad ogni tool contemporaneamente in maniera parallela così da non inficiare la velocità di elaborazione; Aggregherà i risultati e dopo genererà la richiesta iniziale, finito ciò  ci sarà un momento di controllo di adeguatezza dei risultati e la decisione di rifare da capo la generazione o la fuori uscita di essa.

![Grafo strutturale](grafi/Grafo%20strutturale.png)
![Grafo decisionale](grafi\Grafo%20decisionale.png)