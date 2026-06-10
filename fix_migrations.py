"""
Ejecutar desde el directorio del proyecto: python fix_migrations.py
Lee los nombres exactos de migraciones instaladas y reconstruye django_migrations.
"""
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'edfabs.settings'

import django
django.setup()

from django.db import connection

# Directorio base de Django instalado
import django as _dj
django_base = os.path.join(os.path.dirname(_dj.__file__), 'contrib')

CORE_APPS = ['contenttypes', 'auth', 'admin', 'sessions']

with connection.cursor() as cursor:
    cursor.execute('DELETE FROM django_migrations')
    print('django_migrations vaciado.')

    for app in CORE_APPS:
        mig_dir = os.path.join(django_base, app, 'migrations')
        files = sorted(
            f[:-3] for f in os.listdir(mig_dir)
            if f[0].isdigit() and f.endswith('.py')
        )
        for name in files:
            cursor.execute(
                "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, NOW())",
                [app, name]
            )
            print(f'  OK  {app}.{name}')

print('\nListo. Ahora ejecuta:')
print('  python manage.py migrate --fake-initial')
