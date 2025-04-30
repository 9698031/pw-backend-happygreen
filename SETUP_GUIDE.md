# Guida alla Configurazione di HappyGreen Backend

Questa guida ti aiuterà a configurare completamente l'ambiente di sviluppo per il backend di HappyGreen.

## Prerequisiti

Assicurati di avere i seguenti strumenti installati:

- Python 3.9 o superiore
- pip (gestore pacchetti Python)
- Git
- MySQL (opzionale, per la produzione)

## Procedura di Configurazione

### 1. Clona il Repository

```bash
git clone https://github.com/your-username/backend-happygreen.git
cd backend-happygreen
```

### 2. Crea un Ambiente Virtuale

```bash
# Per Windows
python -m venv venv
venv\Scripts\activate

# Per macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Installa le Dipendenze

```bash
pip install -r requirements.txt
```

### 4. Configura il Database

Per sviluppo (SQLite):
```bash
# Configura il database e applica le migrazioni
python manage.py migrate
```

Per produzione (MySQL):
1. Crea un database MySQL:
```sql
CREATE DATABASE pwhappygreen_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'pwhappygreen_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON pwhappygreen_db.* TO 'pwhappygreen_user'@'localhost';
FLUSH PRIVILEGES;
```

2. Modifica il file `backend_happygreen/settings.py` per utilizzare MySQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pwhappygreen_db',
        'USER': 'pwhappygreen_user',
        'PASSWORD': 'password',  # Usa una password sicura!
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

3. Applica le migrazioni:
```bash
python manage.py migrate
```

### 5. Crea un Superuser

```bash
python manage.py createsuperuser
```

### 6. Carica i Dati Iniziali

```bash
python manage.py create_initial_data
```

### 7. Configura le Cartelle per i Media

```bash
# Crea la cartella media e le sue sottocartelle
mkdir -p media/avatars media/badges media/posts media/objects media/products
```

### 8. Avvia il Server di Sviluppo

```bash
python manage.py runserver
```

### 9. Accedi alle Risorse

- Interfaccia Admin: http://127.0.0.1:8000/admin/
- Documentazione API (Swagger): http://127.0.0.1:8000/swagger/
- Documentazione API (ReDoc): http://127.0.0.1:8000/redoc/

## Configurazione per la Produzione

Per la produzione, è consigliabile:

1. Impostare `DEBUG = False` in `settings.py`
2. Generare una nuova SECRET_KEY sicura
3. Configurare ALLOWED_HOSTS con i domini corretti
4. Utilizzare un server web come Nginx o Apache con WSGI (Gunicorn/uWSGI)
5. Configurare HTTPS

### Esempio di Configurazione Nginx

```nginx
server {
    listen 80;
    server_name happygreen-api.example.com;
    
    location /static/ {
        alias /path/to/backend-happygreen/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/backend-happygreen/media/;
    }
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Avviare con Gunicorn

```bash
gunicorn backend_happygreen.wsgi:application --bind 0.0.0.0:8000
```

## Risoluzione Problemi

### Problema: Errore di installazione mysqlclient

Se incontri problemi nell'installazione di mysqlclient:

**Per Ubuntu/Debian:**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```

**Per macOS:**
```bash
brew install mysql-client
export PATH="/usr/local/opt/mysql-client/bin:$PATH"
```

### Problema: Errore di migrazione

Se hai errori durante le migrazioni, prova:
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### Problema: Errore di caricamento immagini

Verifica che le cartelle media siano state create e che abbiano i permessi corretti:
```bash
chmod -R 755 media/
```

## Aggiornamenti e Manutenzione

Per aggiornare il database dopo modifiche ai modelli:
```bash
python manage.py makemigrations
python manage.py migrate
```

Per raccogliere i file statici:
```bash
python manage.py collectstatic
```

Per svuotare la cache:
```bash
python manage.py clearcache  # Richiede django-clear-cache
```