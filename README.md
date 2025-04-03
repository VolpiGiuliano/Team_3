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