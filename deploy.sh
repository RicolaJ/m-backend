#!/bin/bash
# =============================================================
# Script de déploiement M-Motors — PythonAnywhere
# Usage : bash deploy.sh
# À exécuter depuis le répertoire du projet sur PythonAnywhere
# =============================================================

set -e

echo "=== M-Motors Backend — Déploiement ==="

# 1. Pull dernière version
echo "→ Mise à jour du code..."
git pull origin main

# 2. Activer le virtualenv
echo "→ Activation du virtualenv..."
source ~/.virtualenvs/mmotors/bin/activate

# 3. Installer les dépendances
echo "→ Installation des dépendances..."
pip install -r requirements.txt --quiet

# 4. Migrations
echo "→ Application des migrations..."
python manage.py migrate --no-input

# 5. Collecte des fichiers statiques
echo "→ Collecte des fichiers statiques..."
python manage.py collectstatic --no-input --clear

# 6. Charger les fixtures (uniquement si la BDD est vide)
VEHICLE_COUNT=$(python manage.py shell -c "from apps.vehicles.models import Vehicle; print(Vehicle.objects.count())" 2>/dev/null || echo "0")
if [ "$VEHICLE_COUNT" -eq "0" ]; then
    echo "→ Chargement des fixtures de démonstration..."
    python manage.py loaddata fixtures/vehicles.json
else
    echo "→ Données existantes, fixtures ignorées."
fi

# 7. Créer le superuser si défini en env
echo "→ Vérification du superuser..."
python manage.py create_superuser_env

echo ""
echo "✅ Déploiement terminé !"
echo "   Rechargez votre Web App depuis l'onglet PythonAnywhere > Web."
