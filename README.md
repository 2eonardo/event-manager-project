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

---
## Istruzioni installazione e avvio del progetto

---
## Testing Scenario 

---
## DataBase SQLite
Il file di database incluso nel progetto si chiama **`db.sqlite3`**.

All'interno del database sono già presenti 2 account di prova per ogni ruolo, username e password sono riportati nella sezione successiva.
Inoltre il database è già stato popolato con diversi eventi di esempio e categorie di quest'ultimi.
---
## Credenziali di Prova (Demo Accounts)

Per testare le diverse funzionalità e i permessi dell'applicazione direttamente dal browser, utilizzare i seguenti account fittizi già presenti nel database di demo:

### Amministratore (Superuser):
- **Username:** `admin_demo`
- **Password:** `admin12345`
- **Ruolo:** Amministratore del sito (accesso a `/admin`)

### Organizzatori (Organizer):
- **Username:** `demo_organizer1`
- **Password:** `organizer12345`
- **Username:** `demo_organizer2`
- **Password:** `cpx12345`
- **Ruolo:** Organizzatore di eventi

### Partecipant (Attendee):
- **Username:** `demo_attendee1`
- **Password:** `attendee12345`
- **Username:** `demo_attendee2`
- **Password:** `cpx12345`
- **Ruolo:** Utente partecipante standard

---