## Teatrope API – Complete Project Guide

Welcome to Teatrope, a Django REST Framework API that powers a theater discovery and ticketing experience. It provides user management with token auth, content management for theaters, plays and performances, discovery and recommendation records, notifications, and ticket reservations.

### Highlights
- Django 4 + Django REST Framework
- Token-based authentication
- MySQL 8 database
- Dockerized development setup with health checks and startup sequencing

## Quick Start

### Using Docker (Recommended)
```bash
git clone https://github.com/yourusername/teatrope.git
cd teatrope
cp env.example .env
docker compose up -d --build
```

### Local Development (Optional)
```bash
git clone https://github.com/yourusername/teatrope.git
cd teatrope
python -m venv venv
# Activate virtual environment
pip install -r backend/requirements.txt
cd backend
python manage.py runserver
```

## 1) Overview and Requirements

### Context
Teatrope exposes a REST API to:
- Manage users, theaters, plays, casts, and showtimes
- Track user searches and store recommendation results
- Send notifications and persist user preferences
- Create reservations and ticket details

### Requirements
- Docker Desktop (or a Docker environment capable of running Linux containers)
- Docker Compose (integrated with modern Docker Desktop)
- Postman (for testing)

Optional (local development without Docker):
- Python 3.12
- MySQL 8


## 2) Environment Variables

Create a `.env` file at the project root with at least the following variables. Values shown are safe defaults for local development. (IF YOU FOLLOWED THE QUICK START THIS IS ALREADY DONE)

```dotenv
# Django
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*

# MySQL
MYSQL_DATABASE=teatrope
MYSQL_USER=teatrope
MYSQL_PASSWORD=teatrope
MYSQL_ROOT_PASSWORD=rootpass
MYSQL_HOST=db
MYSQL_PORT=3306
```

Notes:
- `MYSQL_HOST` must be `db` (the Compose service name).
- `DJANGO_ALLOWED_HOSTS` can be a comma-separated list; `*` is fine for local dev.


## 3) Run with Docker

### Build and start
```bash
docker compose up -d --build
```

This will:
- Start `db` (MySQL 8) with a healthcheck
- Build and start `web` (Django)
- Wait for DB readiness, auto-generate migrations for local apps, and run migrations
- Expose the API at `http://localhost:8001`

### Logs
```bash
docker compose logs -f db
docker compose logs -f web
```

### Create a superuser (optional)
```bash
docker compose exec web python manage.py createsuperuser
```

### Stop and clean
```bash
docker compose down
```

### Troubleshooting
- If web starts before DB is ready: the entrypoint waits and retries until available.
- If you changed models and need fresh migrations: they are auto-generated on container start; you can also run:
  ```bash
  docker compose exec web python manage.py makemigrations
  docker compose exec web python manage.py migrate
  ```
- If you see “table already exists” for initial migrations, you can reconcile with:
  ```bash
  docker compose exec web python manage.py migrate --fake-initial
  ```


## 4) Apps and Models

### accounts
Custom user model `accounts.Usuario` (auth by email) with fields:
- `id` (UUID, PK)
- `email` (unique, used as username)
- `tipo_rol` (CONSUMIDOR | TEATRO)
- Preference fields: `permisos_json`, `generos_preferidos_json`, `calle_preferida`, `distrito_preferida`, `latitud_preferida`, `longitud_preferida`
- `ultimo_login`

### content
- `Teatro`: basic theater info (name, address, coordinates)
- `Obra`: play linked to `Teatro`, with `genero` and director info
- `Funcion`: performance linked to `Obra` with schedule and seat availability
- `Persona`: cast/crew linked to `Obra` with role

### discovery
- `Busqueda`: user search log/parameters
- `ObraVistaCache`: flattened play info for recommendations
- `Recomendacion`: links a `Busqueda` to an `ObraVistaCache` with a score and reason

### notifications
- `Notificacion`: sent to a `usuario_id` with type, content and state
- `RecomendacionPersonalizada`: ties a recommendation to a notification
- `PreferenciasUsuario`: per-user saved preferences

### tickets
- `Reserva`: reservation for a user and a function, with state and metadata
- `DetalleEntrada`: ticket detail linked to a `Reserva`
- `DisponibilidadCache`: cached seat availability per function


## 5) Base URL and Authentication

- Base URL: `http://localhost:8001/api/`
- Authentication: Token (DRF TokenAuth)
  - Header: `Authorization: Token <YOUR_TOKEN>`


## 6) Endpoints and CRUD with Examples

Below is a concise list of endpoints by app. All standard DRF `ModelViewSet` routes exist unless noted: `list (GET)`, `retrieve (GET)`, `create (POST)`, `update (PUT)`, `partial_update (PATCH)`, `destroy (DELETE)`.

### accounts

Auth routes:
- `POST /api/auth/register/`
- `POST /api/auth/token/login/`
- `POST /api/auth/token/logout/` (requires auth)

User routes (require auth):
- `GET /api/auth/users/`
- `POST /api/auth/users/`
- `GET /api/auth/users/{id}/`
- `PUT /api/auth/users/{id}/`
- `PATCH /api/auth/users/{id}/`
- `DELETE /api/auth/users/{id}/`

Register request:
```json
{
  "email": "user@example.com",
  "password": "StrongPass123",
  "tipo_rol": "CONSUMIDOR"
}
```

Register response (201):
```json
{
  "user": {
    "id": "3d6f2fdc-8c5d-4f87-baa9-8a3b05d5f2a4",
    "email": "user@example.com",
    "tipo_rol": "CONSUMIDOR",
    "permisos_json": [],
    "generos_preferidos_json": [],
    "calle_preferida": "",
    "distrito_preferida": "",
    "latitud_preferida": null,
    "longitud_preferida": null
  },
  "token": "abcd1234..."
}
```

Login request:
```json
{
  "email": "user@example.com",
  "password": "StrongPass123"
}
```

Login response (200):
```json
{
  "token": "abcd1234...",
  "user": {
    "id": "3d6f2fdc-8c5d-4f87-baa9-8a3b05d5f2a4",
    "email": "user@example.com",
    "tipo_rol": "CONSUMIDOR",
    "permisos_json": [],
    "generos_preferidos_json": [],
    "calle_preferida": "",
    "distrito_preferida": "",
    "latitud_preferida": null,
    "longitud_preferida": null
  }
}
```

Logout (204):
```
POST /api/auth/token/logout/
Authorization: Token <YOUR_TOKEN>
```


### content

Routes:
- `Teatro`: `/api/content/teatros/`
- `Obra`: `/api/content/obras/`
- `Funcion`: `/api/content/funciones/`
- `Persona`: `/api/content/personas/`

Create Teatro request:
```json
{
  "nombre": "Teatro Central",
  "descripcion": "Sala principal",
  "calle": "Av. Principal 123",
  "distrito": "Centro",
  "latitud": -12.0464,
  "longitud": -77.0428
}
```

Create Teatro response (201):
```json
{
  "id": "b1a9f4b7-9c9d-4e0f-bf3e-9d7b0b54d2ad",
  "nombre": "Teatro Central",
  "descripcion": "Sala principal",
  "calle": "Av. Principal 123",
  "distrito": "Centro",
  "latitud": -12.0464,
  "longitud": -77.0428
}
```

Create Obra request:
```json
{
  "teatro": "b1a9f4b7-9c9d-4e0f-bf3e-9d7b0b54d2ad",
  "titulo": "Hamlet",
  "genero": "DRAMA",
  "director_nombre": "A. Director",
  "director_rol": "DIRECTOR"
}
```

Create Funcion request:
```json
{
  "obra": "1d5c9c1a-2ea7-41ad-9c5b-5807d7f9e0a1",
  "fecha": "2025-10-10T20:00:00Z",
  "duracion_minutos": 120,
  "disponibilidad_asientos": 100
}
```

Create Persona request:
```json
{
  "obra": "1d5c9c1a-2ea7-41ad-9c5b-5807d7f9e0a1",
  "nombre_completo": "J. Actor",
  "rol": "ACTOR"
}
```


### discovery

Routes:
- `Busqueda`: `/api/discovery/busquedas/`
- `Recomendacion`: `/api/discovery/recomendaciones/`
- `ObraVistaCache`: `/api/discovery/obras-cache/`

Create Busqueda request:
```json
{
  "usuario_id": "3d6f2fdc-8c5d-4f87-baa9-8a3b05d5f2a4",
  "genero_filtro": "COMEDIA",
  "calle_filtro": "Av. 1",
  "distrito_filtro": "Centro",
  "latitud_filtro": -12.05,
  "longitud_filtro": -77.04,
  "fecha_inicio": "2025-10-01T00:00:00Z",
  "fecha_fin": "2025-10-31T23:59:59Z"
}
```

Create Recomendacion request:
```json
{
  "busqueda": "f2f9f7b2-5dd8-4b7b-9ac8-4f5af7b12c7e",
  "obra": "e7b1c5e2-5291-4d40-8b76-889e50927020",
  "puntuacion": 0.92,
  "razon": "Popular cerca de ti"
}
```

Create ObraVistaCache request:
```json
{
  "titulo": "Hamlet",
  "genero": "DRAMA",
  "calle": "Av. Principal 123",
  "distrito": "Centro",
  "latitud": -12.0464,
  "longitud": -77.0428,
  "funciones_json": [
    { "fecha": "2025-10-10T20:00:00Z", "duracion_minutos": 120 }
  ]
}
```


### notifications

Routes:
- `Notificacion`: `/api/notifications/notificaciones/`
- `RecomendacionPersonalizada`: `/api/notifications/recomendaciones-personalizadas/`
- `PreferenciasUsuario`: `/api/notifications/preferencias/`

Create Notificacion request:
```json
{
  "usuario_id": "3d6f2fdc-8c5d-4f87-baa9-8a3b05d5f2a4",
  "tipo": "RECOMENDACION",
  "contenido": "Nueva obra para ti",
  "titulo_mensaje": "Sugerencia",
  "cuerpo_mensaje": "Te puede gustar Hamlet",
  "enlace_mensaje": "https://ejemplo.com/obra/hamlet",
  "estado": "ENVIADA"
}
```

Create PreferenciasUsuario request:
```json
{
  "usuario_id": "3d6f2fdc-8c5d-4f87-baa9-8a3b05d5f2a4",
  "generos_json": ["DRAMA", "COMEDIA"],
  "calle_preferida": "Av. 1",
  "distrito_preferida": "Centro",
  "latitud_preferida": -12.05,
  "longitud_preferida": -77.04,
  "frecuencia_notif": "SEMANAL"
}
```

Create RecomendacionPersonalizada request:
```json
{
  "notificacion": "b9c32d1a-1d0b-4c8a-b0a8-0f21c0b5c0b0",
  "obra_id": "1d5c9c1a-2ea7-41ad-9c5b-5807d7f9e0a1",
  "score_relevancia": 0.85,
  "razon": "Basada en tus preferencias"
}
```


### tickets

Routes:
- `Reserva`: `/api/tickets/reservas/`
- `DetalleEntrada`: `/api/tickets/detalles/`
- `DisponibilidadCache`: `/api/tickets/disponibilidad/`

Create Reserva request:
```json
{
  "usuario_id": "3d6f2fdc-8c5d-4f87-baa9-8a3b05d5f2a4",
  "funcion_id": "2cfc3e0a-9eb5-4a64-bb04-05c0e5b2a7f0",
  "cantidad": 2,
  "estado": "PENDIENTE",
  "codigo_qr": "",
  "detalles_ticket": ""
}
```

Create DetalleEntrada request:
```json
{
  "reserva": "c4b7fb81-09b1-4ed7-a3f5-0e3e4f9a6b6e",
  "asiento": "A-10",
  "precio": 50.0
}
```

Create DisponibilidadCache request:
```json
{
  "funcion_id": "2cfc3e0a-9eb5-4a64-bb04-05c0e5b2a7f0",
  "total_asientos": 120,
  "disponibles": 95
}
```


## 7) Testing with Postman

1. Open Postman and create a new Collection “Teatrope API”. Set a collection variable:
   - `baseUrl` = `http://localhost:8001/api`
2. Create “Register” request:
   - POST `{{baseUrl}}/auth/register/`
   - Body: raw JSON (see example above)
3. Create “Login” request:
   - POST `{{baseUrl}}/auth/token/login/`
   - Body: raw JSON; save returned `token` as a collection variable `authToken`.
4. Set a Collection-level header:
   - Key: `Authorization`
   - Value: `Token {{authToken}}`
5. Add requests for CRUD on each resource under folders:
   - content: teatros, obras, funciones, personas
   - discovery: busquedas, recomendaciones, obras-cache
   - notifications: notificaciones, recomendaciones-personalizadas, preferencias
   - tickets: reservas, detalles, disponibilidad
6. Use the example JSONs from this README for the body payloads.

Tip: you can export/import the collection JSON once set up.


## 8) Useful Admin and Maintenance Commands

```bash
# Open Django shell
docker compose exec web python manage.py shell

# Create superuser
docker compose exec web python manage.py createsuperuser

# Make and apply migrations
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py migrate --fake-initial

# Check URLs
docker compose exec web python manage.py show_urls
```


## 9) Security & Production Notes

- Do not run with `DJANGO_DEBUG=True` in production
- Set a strong `DJANGO_SECRET_KEY`
- Restrict `DJANGO_ALLOWED_HOSTS`
- Use a managed MySQL instance and configure backups
- Add HTTPS, WAF, and proper CORS settings for your client apps


## 10) Project Tree

```text
teatrope/
├── backend/
│   ├── accounts/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── content/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── discovery/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── notifications/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── tickets/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── teatrope/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── docker/
│   │   ├── docker_files/
│   │   │   └── Dockerfile
│   │   └── entrypoints/
│   │       └── entrypoint.sh
│   ├── manage.py
│   └── requirements.txt
├── docker-compose.yml
├── models_reference.txt
├── README.md
├── README2.md
└── venv/
    ├── Include/
    ├── Lib/
    │   └── site-packages/
    │       ├── asgiref/
    │       ├── corsheaders/
    │       ├── django/
    │       ├── djangorestframework/
    │       ├── dotenv/
    │       ├── MySQLdb/
    │       ├── pip/
    │       ├── python_dotenv/
    │       ├── pytz/
    │       ├── rest_framework/
    │       ├── sqlparse/
    │       └── tzdata/
    ├── pyvenv.cfg
    └── Scripts/
        ├── activate
        ├── activate.bat
        ├── Activate.ps1
        ├── deactivate.bat
        ├── django-admin.exe
        ├── dotenv.exe
        ├── pip.exe
        ├── pip3.12.exe
        ├── pip3.exe
        ├── python.exe
        ├── pythonw.exe
        └── sqlformat.exe
```


## 11) Support

If you run into any issue, capture the failing request/response, the `web` and `db` logs, and the payload you sent in Postman, then share them for triage.