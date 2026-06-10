"""
fix_user_fks.py
Detecta todas las apps con FK integer → auth_user, elimina sus tablas
y las recrea correctamente con UUID mediante migrate.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'edfabs.settings'
import django; django.setup()

from django.db import connection
from django.apps import apps as django_apps

SKIP_APPS = {'auth', 'contenttypes', 'admin', 'sessions', 'mundial'}

# 1 — Encontrar tablas con FK integer → auth_user
with connection.cursor() as c:
    c.execute("""
        SELECT DISTINCT kcu.table_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage ccu
            ON ccu.constraint_name = tc.constraint_name
            AND ccu.table_schema = tc.table_schema
        JOIN information_schema.columns col
            ON col.table_name = kcu.table_name
            AND col.column_name = kcu.column_name
            AND col.table_schema = kcu.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
            AND ccu.table_name = 'auth_user'
            AND col.data_type = 'integer'
    """)
    bad_tables = {row[0] for row in c.fetchall()}

if not bad_tables:
    print("No se encontraron tablas con FK integer → auth_user. Nada que hacer.")
    sys.exit(0)

print(f"Tablas con FK integer → auth_user: {sorted(bad_tables)}\n")

# 2 — Mapear tablas a apps de Django
affected_apps = {}
for app_config in django_apps.get_app_configs():
    if app_config.label in SKIP_APPS:
        continue
    for model in app_config.get_models():
        if model._meta.db_table in bad_tables:
            affected_apps[app_config.label] = app_config
            break

print(f"Apps afectadas: {sorted(affected_apps.keys())}\n")

# 3 — Eliminar tablas y registros de migraciones
with connection.cursor() as c:
    for app_label, app_config in affected_apps.items():
        models = list(app_config.get_models())
        # Revertir orden para respetar dependencias FK dentro de la misma app
        tables = [m._meta.db_table for m in reversed(models)]

        print(f"→ {app_label}:")
        for table in tables:
            c.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
            print(f"   DROP TABLE {table}")

        c.execute("DELETE FROM django_migrations WHERE app = %s", [app_label])
        print(f"   Migraciones de '{app_label}' eliminadas del registro\n")

print("Listo. Ahora ejecuta:")
print("  python manage.py migrate")
