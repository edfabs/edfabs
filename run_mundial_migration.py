"""
Ejecutar: python run_mundial_migration.py
Crea las tablas de mundial directamente via schema editor, sin pasar por el executor.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'edfabs.settings'

from django.db.migrations import loader as _loader
_loader.MigrationLoader.check_consistent_history = lambda self, connection: None

import django
django.setup()

from django.db import connection
from django.apps import apps

mundial = apps.get_app_config('mundial')

# Orden necesario: las tablas referenciadas deben existir antes que las que referencian
MODEL_ORDER = [
    'CustomUser',   # base, sin FKs a otras tablas de mundial
    'Team',         # referenciada por Match
    'Match',        # referenciada por Prediction
    'PointConfig',
    'LoginAttempt', # FK a CustomUser
    'Prediction',   # FK a CustomUser y Match
    'UserScore',    # FK a CustomUser
    'AdminLog',     # FK a CustomUser
]

model_map = {m.__name__: m for m in mundial.get_models()}
models = [model_map[n] for n in MODEL_ORDER if n in model_map]

print('Creando tablas de mundial...')
with connection.schema_editor() as schema_editor:
    for model in models:
        try:
            schema_editor.create_model(model)
            print(f'  OK   {model._meta.db_table}')
        except Exception as e:
            msg = str(e).lower()
            if 'already exists' in msg or 'ya existe' in msg:
                print(f'  SKIP {model._meta.db_table} (ya existe)')
            else:
                print(f'  ERR  {model.__name__}: {e}')
                raise

with connection.cursor() as cursor:
    cursor.execute(
        "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, NOW())",
        ['mundial', '0001_initial']
    )

print('\nmundial.0001_initial registrado.')
print('\nAhora ejecuta:')
print('  python manage.py migrate --fake')
print('  python manage.py check')
