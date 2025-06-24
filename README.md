# Ecommerce Project - Dulcis Fabula

Un sito ecommerce completo con:
- Catalogo prodotti con categorie
- Carrello della spesa
- Checkout con pagamento
- Sistema di gestione ordini
- Autenticazione utente con profili
- Ruoli per clienti e manager

## Funzionalità principali

- **Catalogo prodotti**: Naviga prodotti per categoria o cerca prodotti
- **Carrello**: Aggiungi/rimuovi prodotti, modifica quantità
- **Checkout**: Completa l'ordine con dettagli di spedizione
- **Account utente**: Registrazione, login, gestione profilo
- **Ordini**: Cronologia ordini e dettagli
- **Admin**: Pannello di amministrazione per gestire prodotti e ordini

## Installazione

1. Clona il repository
2. Crea un virtual environment: `python -m venv venv`
3. Attiva l'env: `source venv/bin/activate` (Linux/Mac) o `venv\Scripts\activate` (Windows)
4. Installa dipendenze: `pip install -r requirements.txt`
5. Esegui migrazioni: `python manage.py migrate`
6. Carica i dati iniziali: `python manage.py loaddata db.json`
7. Crea un superuser: `python manage.py createsuperuser`
8. Avvia il server: `python manage.py runserver`

## Dati di esempio

Il database precaricato include:
- 3 categorie di prodotti
- 36 prodotti di esempio
- 1 utente manager (con accesso admin / superuser)
  - username: `mariorossi`  
  - email: `mariorossi@gmail.com`  
  - password: `dfgh781!`
- 1 utente cliente
  - username: `mariagreco`  
  - email: `mariagreco@gmail.com`  
  - password: `qwertyu$`

## Attenzione: 
la cartella venv/ non è inclusa nel repository