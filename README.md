# todo-app

## How to Run
1. Create `.env` file with environment variables (see `.env.template`).
2. Run via docker
```bash
docker compose up -d
```
3. Run migrations
```bash
docker compose run todo-app poetry run alembic upgrade head
```
