# Fabian Suchett — Projects

## ⚽ Quiniela Mundial FIFA 2026

Aplicación web de quiniela para el Mundial FIFA 2026, construida con Django 3.0.3.

---

## Stack

| Tecnología | Versión |
|---|---|
| Django | 3.0.3 |
| PostgreSQL + psycopg2-binary | 2.8.5 |
| django-storages + boto3 | AWS S3 |
| Pillow | 9.2.0 |
| whitenoise | 5.1.0 |
| gunicorn | 20.1.0 |
| pytz | 2019.3 |

---

## Variables de Entorno Requeridas

Crea un archivo `.env` (o configura en tu plataforma de despliegue):

```bash
# Django
SECRET_KEY=tu-clave-secreta-larga-y-aleatoria
DJANGO_DEBUG=False

# Base de datos
db_name_edfabs=nombre_db
db_user_edfabs=usuario_db
password_edfabs=contraseña_db
host=localhost
port=5432

# AWS S3 (imágenes/avatars)
AWS_ACCESS_KEY_ID=AKIAXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxx
AWS_STORAGE_BUCKET_NAME_EDFABS=tu-bucket

# Email
EMAIL_USE_TLS=True
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=tu@email.com
EMAIL_HOST_PASSWORD=contraseña-app
EMAIL_PORT=587
DEFAULT_FROM_EMAIL=noreply@quiniela.com
```

---

## Configuración Inicial

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Migraciones

> **Nota importante sobre `AUTH_USER_MODEL`:**
> La app `mundial` reemplaza el modelo de usuario estándar de Django con `mundial.CustomUser`.
> Las apps existentes (`blog`, `members`, etc.) usan `get_user_model()` y apuntarán al nuevo modelo.
> Si tienes datos previos en `auth_user`, necesitas migrar en una base de datos limpia.

```bash
# Base de datos limpia (recomendado para instalación nueva)
python manage.py migrate

# Si tienes una BD existente con auth_user, primero crea una DB nueva
# y luego ejecuta migrate desde cero.
```

### 3. Crear superusuario Admin

```bash
python manage.py createsuperuser
# Email: admin@ejemplo.com
# Full name: Administrador
# Password: (mínimo 8 caracteres)
```

El superusuario se crea con `role=ADMIN` y `is_verified=True` automáticamente.

### 4. Cargar datos del torneo (104 partidos)

```bash
python manage.py seed_tournament
```

Opciones:
```bash
# Recargar desde cero (borra todo)
python manage.py seed_tournament --clear
```

Esto carga:
- 48 equipos (grupos A–L)
- 72 partidos de fase de grupos
- 32 partidos de eliminatorias (equipos vacíos, se asignan conforme avanza el torneo)
- Configuración de puntos por fase

---

## Ejecutar en Desarrollo

```bash
python manage.py runserver
```

Acceder a: `http://127.0.0.1:8000/mundial/`

---

## URLs Principales

| URL | Descripción |
|---|---|
| `/mundial/` | Dashboard (requiere login) |
| `/mundial/registro/` | Registro de usuario |
| `/mundial/login/` | Login |
| `/mundial/partidos/` | Lista de partidos + predicciones |
| `/mundial/tabla/` | Tabla de posiciones |
| `/mundial/mis-predicciones/` | Mis predicciones por fase |
| `/mundial/historial/` | Historial de puntos |
| `/mundial/admin-quiniela/` | Panel de administración (solo ADMIN) |

---

## Panel de Administración (`/mundial/admin-quiniela/`)

Solo accesible para usuarios con `role=ADMIN`.

- **Dashboard**: estadísticas globales + líder actual
- **Partidos**: editar, marcar En Juego, registrar resultado
- **Usuarios**: listar, verificar manualmente, activar/desactivar
- **Puntos**: configurar puntos por fase, recalcular
- **Exportar**: tabla de posiciones y predicciones en CSV

---

## Sistema de Puntos (valores default)

| Fase | Puntos por Acierto |
|---|---|
| Fase de Grupos | 1 |
| Ronda de 32 | 2 |
| Octavos de Final | 3 |
| Cuartos de Final | 4 |
| Semifinal | 6 |
| Tercer Lugar | 4 |
| Final | 10 |

Editables desde el panel admin antes o durante el torneo.

---

## Despliegue en Producción (Heroku / Railway)

### Procfile

```
web: gunicorn edfabs.wsgi --log-file -
```

### Variables adicionales

```bash
DJANGO_DEBUG=False
DATABASE_URL=postgres://...
```

### Staticfiles

```bash
python manage.py collectstatic --noinput
```

Con `whitenoise` configurado, los estáticos se sirven directamente.

---

## Tests

```bash
python manage.py test mundial
```

Cubre:
- Registro de usuarios (validaciones, email duplicado, contraseñas)
- Verificación de email (token válido, inválido, expirado)
- Login y bloqueo por intentos fallidos (5 intentos en 15 min)
- Creación y actualización de predicciones
- Deadline de predicciones (1 hora antes del partido)
- `qualify_predictions()` — calificación correcta/incorrecta/nula
- Asignación de puntos según PointConfig
- `playoff_correct` para desempate
- `recalculate_all_scores()` 
- Tabla de posiciones (acceso y ordenamiento)
- Panel admin (permisos, registrar resultado, exportar CSV)

---

## Notas de Arquitectura

### Migración de AUTH_USER_MODEL

La app `mundial` usa `mundial.CustomUser` como `AUTH_USER_MODEL`. Las apps pre-existentes
(`blog`, `members`, `polls`, etc.) usaban `auth.User` directamente. Se actualizaron para
usar `get_user_model()`, pero sus migraciones existentes deben regenerarse en una DB limpia:

```bash
# Solo si hay conflictos de migraciones:
find . -path "*/migrations/0*.py" -not -path "*/mundial/*" -delete
python manage.py makemigrations
python manage.py migrate
```

### Formato del Mundial 2026

El Mundial FIFA 2026 tendrá **48 equipos**:
- 12 grupos de 4 → 72 partidos de fase de grupos
- Ronda de 32 (16 partidos) + Ronda de 16 (8) + Cuartos (4) + Semis (2) + 3er lugar (1) + Final (1) = 32 partidos KO
- **Total: 104 partidos**
