# Progetto Team 3
## Descrizione funzinamento grafi
**Finalità della struttra**:
Abbiamo pensato a una struttura gerarchica multi-agente con un agente managere gestisce la comprensione, l'elaborazione e il controllo della generazione, gli agenti subordinati servo principalmente per delegare le chiamate ai tool che non richiedono l'uso di un modello e nel caso sia necessario questa struttura permette l'utilizzo di un modello di prestazioni più ristretto e preciso che non inficia troppo sulle prestazione e garantisce comunque il parallelismo per non perdere velocità di elaborazione.

**Finalità della decisione**:
Il grafo decisionale è ciò che usaremo come base per la definizione del loop decisionale langgraph che dovrà compiere l'agente manager. Esso dovrà comprendere l'input manuale e definire di quali tool avrà bisogno e potrà accedere ad ogni tool contemporaneamente in maniera parallela così da non inficiare la velocità di elaborazione; Aggregherà i risultati e dopo genererà la richiesta iniziale, finito ciò  ci sarà un momento di controllo di adeguatezza dei risultati e la decisione di rifare da capo la generazione o la fuori uscita di essa.