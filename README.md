# event-manager-project
---
- **Stutende:** Leonardo Soldani 7139732
- **Tipo di progetto:** Full-Stack Web Application
- **Framework utilizzato:** Django 6.0
- **Deployed version:**
---

## Descrizione del Progetto
La piattaforma consente agli utenti di visualizzare gli eventi in programma e di registrarsi per partecipare. Gli organizzatori possono gestire i propri eventi, monitorare le iscrizioni e aggiornare i dettagli in tempo reale.

---

## Mappa delle Pagine Navigabili

Il sito è strutturato attraverso i seguenti template dinamici, tutti estesi da uno scheletro comune (`base.html`):

1. **`base.html` (Scheletro globale)**: Contiene la barra di navigazione che cambia dinamicamente a seconda che l'utente sia autenticato o meno.
2. **`login.html` (Accedi)**: Form standard di autenticazione per tutti gli utenti.
3. **`signup.html` (Registrati)**: Form di creazione dell'account con selezione del ruolo (Partecipante o Organizzatore).
4. **`event_list.html` (Home Page / Bacheca Globale)**: Mostra tutti gli eventi presenti nel database a chiunque acceda al sito. Per gli organizzatori mostra in aggiunta il tasto "Crea Nuovo Evento".
5. **`event_detail.html` (Dettaglio Evento)**: Mostra i dettagli di un singolo evento. Se l'utente loggato è l'organizzatore dell'evento, mostra anche l'elenco dei partecipanti iscritti; se è un partecipante standard, mostra il pulsante di iscrizione.
6. **`event_form.html` (Crea/Modifica Evento)**: Form dinamico (ModelForm) utilizzato dagli organizzatori per inserire o aggiornare i propri eventi.
7. **`profile.html` (Area Personale)**: Mostra i dati dell'utente, la bio e una lista personalizzata:
   * Gli *Attendee* vedono solo l'elenco degli eventi a cui si sono iscritti.
   * Gli *Organizer* vedono solo l'elenco degli eventi creati da loro.

---
## Funzionalità Implementate
- La registrazione di un nuovo utente avviene tramite il form di registrazione, dove l'utente può scegliere se registrarsi come partecipante o come organizzatore. In base al ruolo scelto, l'utente avrà accesso a funzionalità diverse.

- Il Login può essere effettuato sia tramite Username che tramite email, e una volta autenticato, l'utente viene reindirizzato alla home page (bacheca globale).

- Ciascun utente può modificare i propri dati personali e la propria bio, ma non può modificare il proprio ruolo.

### Organizzatori:
- Creazione eventi con nome, descrizione, luogo, categoria di appartenenza, data e orario.
- Accesso alla bacheca personale dei propri eventi creati.
- Modifica eventi creati, impossibilità di creare eventi con date passate, impossibilità di modificare la data di un evento impostandola nel passato.
- Visualizzazione elenco partecipanti iscritti ai propri eventi.
- Eliminazione eventi creati.

### Partecipanti:
- Visualizzazione degli eventi disponibili con filtri di ricerca avanzati per categoria, data esatta, luogo e ordinamento cronologico.
- Iscrizione agli eventi disponibili, impossibilità di iscriversi a eventi ormai scaduti (data passata).
- Visualizzazione elenco eventi a cui si è iscritti.
- Cancellazione prenotazione da eventi ai quali si è iscritti.
- Possibilità di visitare gli account degli organizzatori e vedere gli eventi che hanno creato.

Gli organizzatori non possono iscriversi agli eventi come i partecipanti, ma presentano tutte le funzionalità di navigazione disponibili per i partecipanti.

---
## Istruzioni installazione e avvio del progetto

---
## Testing Scenario

### Scenario 1: Flusso dell'Organizzatore

Questo scenario testa la creazione di eventi, le regole di validazione (date passate e duplicati), l'elenco privato degli iscritti e la protezione dei permessi di modifica.

1.  **Login come Organizzatore:**
    *   Accedi alla pagina di login e inserisci le credenziali di **`demo_organizer2`** o la mail **`demoorganizer2@gmail.com`** (password: `cpx12345`).
2.  **Verifica creazione eventi:**
    *   Clicca sul tuo username in alto a destra e scorri per creare il tuo primo evento tramite il link `Crea il tuo primo evento`, oppure usa il tasto `+ Crea nuovo evento` presente nella home page e nell'header.
    *   Compila i campi richiesti e clicca su `Crea evento`. Puoi lasciare intenzionalmente alcuni campi vuoti o inserire una data precedente al giorno stesso per verificare i vincoli di validazione.
3.  **Navigazione e modifica:**
    *   Torna alla home page e prova a cliccare su eventi che non sono organizzati da te, poi naviga sul tuo evento personale per notare la differenza.
    *   Modifica il tuo evento cliccandoci sopra dalla home page oppure passando dalla pagina del tuo account (cliccando sul tuo username) e premendo infine sul tasto `Modifica`.
    *   Puoi verificare nuovamente i vincoli sulle date passate esattamente come fatto in fase di creazione.
4.  **Eliminazione:**
    *   Naviga all'interno della pagina per raggiungere la schermata del tuo evento e procedi con l'eliminazione definitiva.

L'organizzatore **`demo_organizer1`** è il creatore di tutti gli eventi presenti. Il flusso di test può essere eseguito anche tramite questo account, notando la lista completa delle sue creazioni all'interno della pagina del suo profilo. Le credenziali complete sono presenti nei capitoli successivi.

### Scenario 2: Flusso del Partecipante

Questo scenario testa la ricerca degli eventi con filtri avanzati, l'iscrizione, la gestione dei ticket nel profilo e la cancellazione della prenotazione.

1.  **Login come Partecipante:**
    *   Accedi alla pagina di login ed entra con un account Partecipante.
2.  **Test dei Filtri di ricerca:**
    *   Dalla Home Page, usa il modulo di filtraggio: seleziona la categoria dell'evento, digita la città nel campo `Luogo` oppure imposta una data di ricerca e clicca su **`Filtra`**.
    *   Verifica che la bacheca mostri solo gli eventi corrispondenti ai filtri applicati. Clicca su **`Azzera`** per ripristinare la visualizzazione completa.
    *   Se utilizzi filtri che non corrispondono a nessun evento attivo, non verrà mostrato alcun evento.
3.  **Iscrizione all'evento:**
    *   Clicca su un evento attivo per aprirne il dettaglio.
    *   Clicca sul pulsante verde **`Iscriviti all'evento`**.
4.  **Verifica dei Ticket nell'Area Personale:**
    *   Clicca sul tuo nome in alto a destra nella barra di navigazione per accedere alla tua **Area Personale**.
    *   Nella sezione *"I Miei Ticket (Eventi a cui sono iscritto)"* troverai la scheda dell'evento a cui ti sei appena registrato.
5.  **Cancellazione dell'iscrizione (Disiscrizione):**
    *   Navigando sull'evento a cui sei iscritto (sia dalla home page che dall'area personale), clicca sul pulsante rosso **`Annulla Iscrizione`** per cancellare la tua iscrizione.
---
## DataBase SQLite
Il file di database incluso nel progetto si chiama **`db.sqlite3`**.

All'interno del database sono già presenti 2 account di prova per ogni ruolo, username, email e password sono riportati nella sezione successiva.
Inoltre il database è già stato popolato con diversi eventi di esempio e categorie di quest'ultimi.
---
## Credenziali di Prova (Demo Accounts)

### Amministratore (Superuser):
- **Username:** `admin_demo`
- **Password:** `admin12345`
- **Ruolo:** Amministratore del sito (accesso a `/admin`)

### Organizzatori (Organizer):
- **Username:** `demo_organizer1`
- **Email:** `demoorganizer1@gmail.com`
- **Password:** `organizer12345`
- **Username:** `demo_organizer2`
- **Email:** `demoorganizer2@gmail.com`
- **Password:** `cpx12345`
- **Ruolo:** Organizzatore di eventi

### Partecipanti (Attendee):
- **Username:** `demo_attendee1`
- **Email:** `demoattendee1@gmail.com`
- **Password:** `attendee12345`
- **Username:** `demo_attendee2`
- **Email:** `demoattendee2@gmail.com`
- **Password:** `cpx12345`
- **Ruolo:** Utente partecipante standard

---