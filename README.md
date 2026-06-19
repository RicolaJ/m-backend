# M-Motors — Backend (Django REST Framework)

API REST du projet M-Motors. Gestion des véhicules, dossiers clients, authentification JWT.

## Stack
- **Django 4.2** + **Django REST Framework**
- **PostgreSQL** (via `dj-database-url`)
- **JWT** (djangorestframework-simplejwt)
- **WhiteNoise** (fichiers statiques)
- **Déploiement** : PythonAnywhere

## Endpoints API

### Auth — `/api/auth/`
| Méthode | URL | Description |
|---------|-----|-------------|
| POST | `/api/auth/token/` | Login → access + refresh tokens |
| POST | `/api/auth/token/refresh/` | Rafraîchir le token |
| POST | `/api/auth/register/` | Créer un compte |
| GET/PATCH | `/api/auth/me/` | Profil utilisateur |

### Véhicules — `/api/vehicles/`
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/vehicles/` | Liste (filtres: type, motorisation, search, prix__lte) |
| GET | `/api/vehicles/{id}/` | Détail |
| POST | `/api/vehicles/` | Créer (admin) |
| PATCH | `/api/vehicles/{id}/` | Modifier (admin) |
| DELETE | `/api/vehicles/{id}/` | Supprimer (admin) |
| POST | `/api/vehicles/{id}/switch_type/` | Basculer achat ↔ location (admin) |

### Dossiers clients — `/api/dossiers/`
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/dossiers/` | Mes dossiers |
| POST | `/api/dossiers/` | Créer un dossier |
| GET | `/api/dossiers/{id}/` | Détail dossier |
| POST | `/api/dossiers/{id}/upload_document/` | Ajouter un document |

### Admin dossiers — `/api/admin/dossiers/`
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/admin/dossiers/` | Tous les dossiers (admin) |
| POST | `/api/admin/dossiers/{id}/valider/` | Valider |
| POST | `/api/admin/dossiers/{id}/refuser/` | Refuser (+ motif) |
| POST | `/api/admin/dossiers/{id}/en_cours/` | Passer en instruction |

## Installation locale

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Éditez .env avec vos valeurs
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Déploiement PythonAnywhere

1. **Uploader le code** via git clone ou ZIP dans `/home/votre-username/m-motors-backend`

2. **Créer un virtualenv** :
   ```bash
   mkvirtualenv mmotors --python=python3.11
   pip install -r requirements.txt
   ```

3. **Créer le fichier `.env`** à partir de `.env.example`

4. **Configurer la Web App** (onglet Web) :
   - Framework : Django
   - Source code : `/home/votre-username/m-motors-backend`
   - Virtualenv : `/home/votre-username/.virtualenvs/mmotors`
   - WSGI file : copiez le contenu de `pythonanywhere_wsgi.py`

5. **Migrations et static files** :
   ```bash
   python manage.py migrate
   python manage.py collectstatic --no-input
   python manage.py createsuperuser
   ```

6. **Variables d'environnement** : ajoutez-les dans l'onglet Web > Environment variables

7. Reload l'app depuis l'onglet Web.

## PostgreSQL

PythonAnywhere propose PostgreSQL sur les plans payants.
Créez votre base depuis l'onglet "Databases", puis renseignez `DATABASE_URL` dans `.env`.

Format : `postgresql://USER:PASSWORD@votre-username-db-host:PORT/DBNAME`
