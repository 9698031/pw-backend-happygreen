# HappyGreen - Backend Django REST

Backend per l'applicazione Android HappyGreen sulla sostenibilità ambientale.

## Descrizione del Progetto

HappyGreen è un'applicazione che consente agli studenti di diventare più consapevoli dell'ambiente e di divertirsi nel farlo, utilizzando la tecnologia e l'intelligenza artificiale. L'app utilizza il Machine Learning per riconoscere oggetti nell'ambiente e fornisce informazioni educative su come prendersi cura del pianeta.

## Funzionalità implementate

- Registrazione e autenticazione utenti
- Creazione e gestione di gruppi di amici
- Condivisione di foto e luoghi tramite post
- Riconoscimento di oggetti e informazioni sulla sostenibilità
- Quiz e sfide sulla sostenibilità ambientale
- Scanner di codici a barre per prodotti Eco-Friendly
- Sistema di badge e punteggi per gamification

## Requisiti Tecnici

- Python 3.9 o superiore
- Django 5.2
- Django REST Framework
- MySQL (in produzione) / SQLite (in sviluppo)

## Installazione

1. Clona il repository:
```bash
git clone https://github.com/your-username/backend-happygreen.git
cd backend-happygreen
```

2. Crea e attiva un ambiente virtuale:
```bash
python -m venv venv
source venv/bin/activate  # Per Linux/Mac
venv\Scripts\activate  # Per Windows
```

3. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

4. Configura il database:
```bash
python manage.py migrate
```

5. Crea un superuser:
```bash
python manage.py createsuperuser
```

6. Carica i dati iniziali:
```bash
python manage.py create_initial_data
```

7. Avvia il server:
```bash
python manage.py runserver
```

## API Endpoints

Il backend espone le seguenti API:

- `/api/users/`: Gestione utenti
- `/api/profiles/`: Profili utente
- `/api/badges/`: Badge e achievement
- `/api/groups/`: Gruppi di amici
- `/api/posts/`: Post condivisi nei gruppi
- `/api/comments/`: Commenti ai post
- `/api/objects/`: Oggetti riconoscibili
- `/api/scans/`: Registrazioni scansioni oggetti
- `/api/quizzes/`: Quiz sulla sostenibilità
- `/api/challenges/`: Sfide ecologiche
- `/api/products/`: Prodotti scansionabili con barcode

Per una documentazione completa delle API, visita:
- `/swagger/`: Documentazione Swagger UI
- `/redoc/`: Documentazione ReDoc

## Autenticazione

L'API utilizza JWT (JSON Web Token) per l'autenticazione. Ottieni un token tramite:

```
POST /api/token/
{
  "username": "your_username",
  "password": "your_password"
}
```

Utilizza il token nelle richieste successive includendo l'header:
```
Authorization: Bearer <token>
```

## Configurazione del Database per la Produzione

Per utilizzare MySQL in produzione, modifica le impostazioni del database in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pwhappygreen_db',
        'USER': 'pwhappygreen_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

## Contribuire

1. Fai il fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/amazing-feature`)
3. Fai il commit delle tue modifiche (`git commit -m 'Aggiunta una nuova feature'`)
4. Fai il push al branch (`git push origin feature/amazing-feature`)
5. Apri una Pull Request

## Licenza

Distribuito con licenza MIT. Vedi `LICENSE` per ulteriori informazioni.

## Contatti

Nome del progetto: [HappyGreen](https://github.com/your-username/backend-happygreen)