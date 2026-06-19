# ============================================================
# Fichier WSGI pour PythonAnywhere
# Chemin à configurer dans l'onglet "Web" > WSGI configuration file
# ============================================================

import sys
import os

# 1. Remplacez 'votre-username' par votre nom d'utilisateur PythonAnywhere
# 2. Remplacez 'mmotors' par le nom de votre virtualenv si différent

USERNAME = 'votre-username'
PROJECT_PATH = f'/home/{USERNAME}/m-motors-backend'
VENV_PATH = f'/home/{USERNAME}/.virtualenvs/mmotors'

# Ajouter le projet au PYTHONPATH
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

# Activer le virtualenv
activate_env = os.path.join(VENV_PATH, 'bin', 'activate_this.py')
with open(activate_env) as f:
    exec(f.read(), {'__file__': activate_env})

# Pointer vers les settings Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mmotors.settings'

# Charger l'app WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
