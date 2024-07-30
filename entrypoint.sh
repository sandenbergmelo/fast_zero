#!/usr/bin/env sh

# Executa as migrações do banco de dados
poetry run alembic upgrade head

# Inicia a aplicação
poetry run fastapi run --host 0.0.0.0 fast_zero/app.py
