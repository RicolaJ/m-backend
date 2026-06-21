# M-Motors — Backend

> API REST du projet M-Motors — gestion des véhicules, dossiers clients et authentification JWT.  
> Déployé sur **PythonAnywhere** · Base de données **PostgreSQL** · Notifications email via **Brevo**

---

## Sommaire

- [Présentation](#présentation)
- [Stack technique](#stack-technique)
- [Architecture du projet](#architecture-du-projet)
- [Endpoints API](#endpoints-api)
- [Installation locale](#installation-locale)
- [Variables d'environnement](#variables-denvironnement)
- [Tests unitaires](#tests-unitaires)
- [Déploiement PythonAnywhere](#déploiement-pythonanywhere)
- [Notifications email Brevo](#notifications-email-brevo)

---

## Présentation

Backend Django REST Framework du projet M-Motors. Il expose une API complète pour :

- **Authentification** JWT (login, register, refresh token)
- **Gestion des véhicules** (achat / location LDA) avec upload d'images
- **Gestion des dossiers** clients 100% dématérialisés (dépôt, upload de documents, suivi de statut)
- **Back-office admin** (validation/refus des dossiers, CRUD véhicules)
- **Notifications email** automatiques via Brevo à chaque changement de statut de dossier

---

## Stack technique

| Outil | Version | Rôle |
|-------|---------|------|
| Python | 3.10 | Langage |
| Django | 4.2 | Framework web |
| Django REST Framework | 3.15 | API REST |
| djangorestframework-simplejwt | 5.3 | Authentification JWT |
| django-cors-headers | 4.3 | Gestion CORS |
| PostgreSQL | 12 | Base de données |
| psycopg2-binary | 2.9 | Connecteur PostgreSQL |
| dj-database-url | 2.1 | Parsing de DATABASE_URL |
| Pillow | 9.5 | Traitement des images |
| WhiteNoise | 6.6 | Fichiers statiques |
| python-decouple | 3.8 | Variables d'environnement |
| django-filter | 24.2 | Filtres API |

---

## Architecture du projet

```
m-motors-backend/
├── mmotors/                    # Configuration principale Django
│   ├── settings.py             # Settings (DB, JWT, CORS, email...)
│   ├── urls.py                 # URLs racine
│   ├── wsgi.py                 # Point d'entrée WSGI
│   └── email_service.py        # Service email Brevo (valider/refuser/en cours)
├── apps/
│   ├── accounts/               # App utilisateurs
│   │   ├── models.py           # User custom (email comme login)
│   │   ├── serializers.py      # UserSerializer, RegisterSerializer
│   │   ├── views.py            # RegisterView, MeView
│   │   ├── urls.py             # Routes auth
│   │   ├── admin.py            # Admin Django
│   │   ├── migrations/         # Migrations base de données
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── create_superuser_env.py  # Commande création superuser
│   │   └── tests/
│   │       └── test_auth.py    # Tests authentification (7 tests)
│   ├── vehicles/               # App véhicules
│   │   ├── models.py           # Vehicle, VehicleImage
│   │   ├── serializers.py      # VehicleSerializer, VehicleWriteSerializer
│   │   ├── views.py            # VehicleViewSet (CRUD + switch_type)
│   │   ├── urls.py             # Routes véhicules
│   │   ├── admin.py            # Admin Django
│   │   ├── migrations/         # Migrations base de données
│   │   └── tests/
│   │       └── test_vehicles.py  # Tests véhicules (10 tests)
│   └── dossiers/               # App dossiers clients
│       ├── models.py           # Dossier, DossierDocument
│       ├── serializers.py      # DossierSerializer, DossierCreateSerializer
│       ├── views.py            # DossierViewSet, AdminDossierViewSet
│       ├── urls.py             # Routes dossiers (client)
│       ├── admin_urls.py       # Routes dossiers (admin)
│       ├── admin.py            # Admin Django
│       ├── migrations/         # Migrations base de données
│       └── tests/
│           └── test_dossiers.py  # Tests dossiers (11 tests)
├── fixtures/
│   └── vehicles.json           # 12 véhicules de démonstration
├── media/                      # Fichiers uploadés (images, documents)
├── staticfiles/                # Fichiers statiques collectés
├── manage.py                   # CLI Django
├── requirements.txt            # Dépendances Python
├── deploy.sh                   # Script de déploiement automatique
├── pythonanywhere_wsgi.py      # Config WSGI PythonAnywhere
└── .env.example                # Exemple de variables d'environnement
```

---

## Endpoints API

### Authentification — `/api/auth/`

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| POST | `/api/auth/token/` | Login → access + refresh tokens | Non |
| POST | `/api/auth/token/refresh/` | Rafraîchir le token access | Non |
| POST | `/api/auth/register/` | Créer un compte client | Non |
| GET | `/api/auth/me/` | Profil de l'utilisateur connecté | Oui |
| PATCH | `/api/auth/me/` | Modifier le profil | Oui |

### Véhicules — `/api/vehicles/`

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/vehicles/` | Liste des véhicules disponibles | Non |
| GET | `/api/vehicles/{id}/` | Détail d'un véhicule | Non |
| POST | `/api/vehicles/` | Créer un véhicule | Admin |
| PATCH | `/api/vehicles/{id}/` | Modifier un véhicule | Admin |
| DELETE | `/api/vehicles/{id}/` | Supprimer un véhicule | Admin |
| POST | `/api/vehicles/{id}/switch_type/` | Basculer achat ↔ location | Admin |

**Filtres disponibles sur `GET /api/vehicles/` :**

| Paramètre | Description | Exemple |
|-----------|-------------|---------|
| `type` | Filtrer par type | `?type=achat` ou `?type=location` |
| `search` | Recherche texte | `?search=renault` |
| `prix__lte` | Prix maximum | `?prix__lte=15000` |
| `motorisation` | Type de motorisation | `?motorisation=electrique` |

### Dossiers clients — `/api/dossiers/`

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/dossiers/` | Mes dossiers | Oui |
| POST | `/api/dossiers/` | Créer un dossier | Oui |
| GET | `/api/dossiers/{id}/` | Détail d'un dossier | Oui |
| POST | `/api/dossiers/{id}/upload_document/` | Uploader un document | Oui |

### Administration — `/api/admin/dossiers/`

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/admin/dossiers/` | Tous les dossiers | Admin |
| GET | `/api/admin/dossiers/{id}/` | Détail d'un dossier | Admin |
| POST | `/api/admin/dossiers/{id}/valider/` | Valider un dossier | Admin |
| POST | `/api/admin/dossiers/{id}/refuser/` | Refuser un dossier (+ motif) | Admin |
| POST | `/api/admin/dossiers/{id}/en_cours/` | Passer en instruction | Admin |

---

## Installation locale

### Prérequis

- Python 3.10+
- PostgreSQL 12+

### Étapes

```bash
# 1. Cloner le repo
git clone https://github.com/RicolaJ/m-backend.git
cd m-backend

# 2. Créer et activer le virtualenv
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditez .env avec vos valeurs

# 5. Créer la base de données PostgreSQL
createdb mmotors_db

# 6. Appliquer les migrations
python manage.py migrate

# 7. Charger les données de démonstration
python manage.py loaddata fixtures/vehicles.json

# 8. Créer un superuser
python manage.py createsuperuser

# 9. Lancer le serveur
python manage.py runserver
```

L'API est accessible sur `http://localhost:8000/api/`.
L'admin Django sur `http://localhost:8000/admin/`.

---

## Variables d'environnement

Créez un fichier `.env` à la racine (voir `.env.example`) :

```env
# Django
SECRET_KEY=votre-secret-key-longue-et-aleatoire
DEBUG=False
ALLOWED_HOSTS=votre-app.pythonanywhere.com,localhost

# Base de données PostgreSQL
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DBNAME
DATABASE_SSL=False

# CORS — URL du frontend
CORS_ALLOWED_ORIGINS=https://votre-app.netlify.app

# Superuser automatique (déploiement)
DJANGO_SUPERUSER_EMAIL=admin@m-motors.fr
DJANGO_SUPERUSER_PASSWORD=VotreMotDePasseAdmin!

# Email — Brevo SMTP
EMAIL_HOST=smtp-relay.brevo.com
EMAIL_PORT=587
EMAIL_HOST_USER=votre-login@smtp-brevo.com
EMAIL_HOST_PASSWORD=votre-cle-smtp-brevo
DEFAULT_FROM_EMAIL=noreply@m-motors.fr
```

> ⚠️ Ne jamais committer le fichier `.env` — il est dans le `.gitignore`.

Pour générer une `SECRET_KEY` solide :

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## Tests unitaires

### Lancer les tests

```bash
# Tous les tests
python manage.py test apps

# Une app spécifique
python manage.py test apps.accounts
python manage.py test apps.vehicles
python manage.py test apps.dossiers

# Avec verbosité
python manage.py test apps --verbosity=2
```

### Structure des tests

```
apps/
├── accounts/tests/
│   └── test_auth.py        # Inscription, login, token, profil (7 tests)
├── vehicles/tests/
│   └── test_vehicles.py    # CRUD, filtres, switch type, permissions (10 tests)
└── dossiers/tests/
    └── test_dossiers.py    # Création, isolation client, validation admin (11 tests)
```

**Total : 28 tests · 3 suites**

### Ce qui est testé

**Accounts (7 tests)**
- Inscription réussie et email dupliqué
- Login avec bon/mauvais mot de passe
- Accès au profil authentifié/non authentifié
- Validation du mot de passe faible

**Vehicles (10 tests)**
- Liste publique (véhicules indisponibles exclus)
- Filtres par type, recherche, prix maximum
- CRUD admin (création, suppression)
- Switch achat ↔ location
- Permissions (non-admin ne peut pas créer)

**Dossiers (11 tests)**
- Création dossier achat et location avec options
- Isolation des données (client ne voit que ses dossiers)
- Unicité des références de dossier
- Actions admin (valider, refuser, en cours)
- Permissions (non-admin ne peut pas accéder aux endpoints admin)
- Filtrage par statut

---

## Déploiement PythonAnywhere

### Première installation

```bash
# 1. Cloner le repo
git clone https://github.com/RicolaJ/m-backend.git ~/motorsss

# 2. Créer le virtualenv
mkvirtualenv mmotors --python=python3.10
workon mmotors

# 3. Installer les dépendances
cd ~/motorsss
pip install -r requirements.txt

# 4. Créer le fichier .env
cp .env.example .env
nano .env  # Remplir avec les vraies valeurs

# 5. Lancer le script de déploiement
bash deploy.sh
```

### Script deploy.sh

Le script `deploy.sh` automatise le déploiement complet :

```bash
bash deploy.sh
```

Il enchaîne automatiquement :
1. `git pull origin main`
2. `pip install -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py collectstatic`
5. Chargement des fixtures si la base est vide
6. Création du superuser depuis les variables d'environnement

### Configuration WSGI

Dans l'onglet **Web** de PythonAnywhere, le fichier WSGI doit contenir :

```python
import sys, os

PROJECT_PATH = '/home/superwebman/motorsss'
VENV_PATH = '/home/superwebman/.virtualenvs/mon_virtualenv'

if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

activate_env = os.path.join(VENV_PATH, 'bin', 'activate_this.py')
with open(activate_env) as f:
    exec(f.read(), {'__file__': activate_env})

os.environ['DJANGO_SETTINGS_MODULE'] = 'mmotors.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Fichiers statiques et media

Dans l'onglet **Web** → **Static files** :

| URL | Répertoire |
|-----|------------|
| `/static/` | `/home/superwebman/motorsss/staticfiles` |
| `/media/` | `/home/superwebman/motorsss/media` |

### Mises à jour

```bash
workon mmotors
cd ~/motorsss
bash deploy.sh
# Puis Reload dans l'onglet Web
```

---

## Notifications email Brevo

À chaque changement de statut de dossier, un email est automatiquement envoyé au client.

| Événement | Email envoyé |
|-----------|-------------|
| Dossier validé | ✅ Email de félicitations avec lien vers le dossier |
| Dossier refusé | ❌ Email avec motif de refus et lien vers le catalogue |
| Dossier en instruction | 📋 Email de confirmation avec lien de suivi |

### Configuration

1. Créez un compte sur **brevo.com**
2. Allez dans **SMTP & API** → **SMTP** → générez une clé SMTP
3. Ajoutez dans votre `.env` :

```env
EMAIL_HOST=smtp-relay.brevo.com
EMAIL_PORT=587
EMAIL_HOST_USER=votre-login@smtp-brevo.com
EMAIL_HOST_PASSWORD=votre-cle-smtp
DEFAULT_FROM_EMAIL=noreply@m-motors.fr
```

### Tester l'envoi d'email

```bash
workon mmotors
cd ~/motorsss
python manage.py shell -c "
from django.core.mail import send_mail
send_mail('Test M-Motors', 'Email de test', 'noreply@m-motors.fr', ['votre@email.com'], fail_silently=False)
print('OK')
"
```

---

## Modèles de données

### User

```
email (unique)    — identifiant de connexion
first_name        — prénom
last_name         — nom
phone             — téléphone (optionnel)
is_staff          — accès back-office admin
```

### Vehicle

```
marque            — marque du véhicule
modele            — modèle
annee             — année
kilometrage       — kilométrage
prix              — prix de vente
loyer_mensuel     — loyer mensuel (location uniquement)
motorisation      — essence / diesel / hybride / electrique / gpl
couleur           — couleur
type              — achat / location
disponible        — visible dans le catalogue
```

### Dossier

```
reference         — référence unique (MM-XXXXXXXX)
client            — FK User
vehicle           — FK Vehicle
type              — achat / location
statut            — en_attente / en_cours / valide / refuse
message           — message optionnel du client
motif_refus       — motif de refus (admin)
assurance         — option assurance tous risques
assistance        — option assistance dépannage
entretien         — option entretien & SAV
controle_technique — option contrôle technique
```

### DossierDocument

```
dossier           — FK Dossier
nom               — nom du document
fichier           — fichier uploadé
uploaded_at       — date d'upload
```

---
## Monitoring — Sentry

Le backend est connecté à **Sentry** pour la surveillance des erreurs en production.

### Ce que Sentry capture
- Exceptions Django non gérées
- Erreurs 500
- Requêtes lentes
- Erreurs dans les actions admin (validation/refus de dossiers)

### Configuration
Le SDK est initialisé dans `mmotors/settings.py` via l'intégration Django officielle.

La variable d'environnement requise :
```env
SENTRY_DSN=https://xxxx@xxxx.ingest.de.sentry.io/xxxx
```

À ajouter dans le fichier `.env` sur PythonAnywhere.

### Tester
```bash
workon mon_virtualenv
cd ~/motorsss
python manage.py shell -c "
import sentry_sdk
sentry_sdk.capture_message('Test', level='info')
print('OK')
"
```

Vérifiez dans **sentry.io → projet m-motors-backend → Issues**.

## Auteur

Projet réalisé dans le cadre du **Bloc 3 — Développement Python**  
Entreprise : **M-Motors** — Spécialiste véhicules d'occasion depuis 1987
