# Progetto Team 3
## Modello per questionario MIFID
**Finalità del modello**: somministrare un questionario personalizzato sulla base delle risposte del cliente accettando input di testo (non domande a risposta chiusa come è previsto dai questionari standard); confrontare il profilo di conoscenza ed esperienza con il grado di complessità dello strumento/prodotto finanziario in questione; fornire delle indicazioni sui prodotti maggiormente compatibili con il profilo del cliente.
La direttiva europea MiFID impone alle banche determinati obblighi di trasparenza e comunicazione nei confronti dei clienti al dettaglio, ovvero coloro caratterizzati da minore conoscenza ed esperienza in ambito di investimenti. Quando vengono richiesti da parte del cliente servizi ad elevato valore aggiunto (consulenza in materia di investimenti o gestione di portafoglio), la banca è tenuta ad effettuare una valutazione di adeguatezza degli strumenti finanziari proposti. Per questi servizi la normativa ha previsto l’obbligo di verifica di adeguatezza. L’intermediario è pertanto tenuto a raccogliere informazioni relative a:
1. Conoscenza ed esperienza nel settore di investimento rilevante per il tipo di strumento/servizio.
    - servizi/operazioni/strumenti finanziari con i quali il cliente ha dimestichezza
    - natura/volume/holding-period/frequenza delle operazioni realizzate
    - livello di istruzione e professione o, se rilevante, precedente professione
2. Situazione finanziaria
    - fonte e consistenza del reddito regolare
    - attività, comprese le attività liquide
    - investimenti e beni immobili
    - impegni finanziari regolari
3. Obiettivi di investimento
    - holding period
    - preferenze in materia di rischio
    - finalità dell’investimento
Queste rappresentano sostanzialmente le sezioni in cui si articola il questionario MiFID
Sulla base delle informazioni ricevute dal cliente, gli intermediari valutano se lo specifico servizio/strumento sia adeguato, ossia: corrispondenza agli obiettivi di investimento del cliente, comprensione dell’esposizione al rischio, capacità di sopportare il rischio associato all’investimento.

## Descrizione contenuto
- Docker presenti
    - docker python
    - docker ollama
- Docker-compose: crea la rete condivisa per poter far parlare i docker tra di loro localmente
- Dockerfile dello script python: crea l'immagine del docker per far girare lo script python
- script python: comunica con l'api di ollama per sfruttare il modello installato