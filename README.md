# Demo App Backend

FastAPI backend for working with banners and news.

The project already includes:
- FastAPI
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- SQLAdmin
- MinIO as S3-compatible storage for images

## Current features

- `GET /` returns `OK`
- `GET /banners` returns only active banners
- `GET /news` returns only active news
- admin panel at `/admin`
- create and edit banners and news from admin panel
- image upload to MinIO from admin panel
- API returns `image` as a public MinIO URL

## Stack

- Python `3.13`
- FastAPI
- SQLAlchemy `2.x`
- Alembic
- PostgreSQL
- SQLAdmin
- MinIO
- `uv` for dependency management

## Project structure

```text
src/
  admin.py
  config.py
  db.py
  main.py
  session.py
  storage.py
  basic/
    views/
      router.py
    domain/
      controller.py
      schemas.py
    data/
      models.py
      repositories.py
alembic/
templates/
```

Layered architecture:
- `views` - FastAPI routes
- `domain` - business logic and pydantic schemas
- `data` - SQLAlchemy models and repositories

## Environment variables

The app reads settings from `.env`.

Main variables:

```env
POSTGRES_PORT=5432
POSTGRES_USER=string
POSTGRES_PASSWORD=string
POSTGRES_HOST=localhost
POSTGRES_DB=demo_app

S3_ACCESS_KEY=string
S3_SECRET_KEY=string
S3_HOST=localhost
S3_PORT=9000
S3_BUCKET=demoapp
S3_SECURE=False
S3_TYPE=minio

ADMIN_USERNAME=string
ADMIN_PASSWORD=string
ADMIN_SECRET_KEY=string
```

## Local run

### 1. Install dependencies

```powershell
uv sync
```

### 2. Start PostgreSQL and MinIO

You can use local services or Docker Compose.

### 3. Apply migrations

```powershell
uv run alembic upgrade head
```

### 4. Start the app

```powershell
uv run uvicorn src.main:app --reload
```

After startup:
- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Admin: `http://127.0.0.1:8000/admin`

## Docker Compose

Project files:
- `Dockerfile`
- `Dockerfile.minio`
- `docker-compose.yml`

Run:

```powershell
docker compose up --build
```

Services:
- app: `http://localhost:8000`
- postgres: `localhost:5432`
- minio api: `http://localhost:9000`
- minio console: `http://localhost:9001`

Important:
- inside Docker Compose the app connects to Postgres via host `db`
- inside Docker Compose the app connects to MinIO via host `minio`
- this is already configured in `docker-compose.yml`

## Admin panel

Admin panel URL:

```text
http://127.0.0.1:8000/admin
```

Credentials are read from `.env`:
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`

Admin panel supports:
- create banners
- edit banners
- create news
- edit news
- toggle `active`
- upload image
- image preview in list, details and edit pages

## Banner model

Current fields:
- `id`
- `created_at`
- `updated_at`
- `image`
- `position`
- `name`
- `description`
- `active`

Rules:
- `image` is required
- `position` default is `0`
- `name` and `description` are optional
- `active` default is `False`
- banners are sorted by `position DESC`, then `id DESC`
- `/banners` returns only active banners

## News model

Current fields:
- `id`
- `created_at`
- `updated_at`
- `image`
- `position`
- `name`
- `description`
- `active`

Rules:
- `image` is optional
- `position` default is `0`
- `name` and `description` are optional
- `active` default is `False`
- news are sorted by `position DESC`, then `id DESC`
- `/news` returns only active news
- `/news` returns at most `10` records

## Images and MinIO

Images are uploaded to MinIO through `sqladmin` and `fastapi-storages`.

Upload flow:
- file is stored in bucket `demoapp`
- original filename is replaced with `UUID`
- extension is preserved
- database stores object key
- API returns a full public image URL

On app startup:
- bucket is created automatically if missing
- bucket policy is set for public object reads

## Migrations

Create migration:

```powershell
uv run alembic revision --autogenerate -m "message"
```

Apply migrations:

```powershell
uv run alembic upgrade head
```

Rollback one migration:

```powershell
uv run alembic downgrade -1
```

## Useful URLs

- `GET /`
- `GET /banners`
- `GET /news`
- `GET /docs`
- `GET /admin`

## Notes

- runtime DB access uses `asyncpg`
- Alembic and sync tasks use `psycopg`
- admin panel is protected with simple login/password from `.env`
- `.env` is ignored by git, so it is a good idea to add `.env.example`
