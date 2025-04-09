#!/bin/bash
# Activate virtual environment

echo Installing dependencies
uv pip install --system -e .

echo Initializing database
uv run init_db
echo DONE

# printenv

echo Pulling tokens
uv run pull_tokens
echo DONE

uvicorn qrypt.main:app --host 0.0.0.0 --port 8000 &

streamlit run src/qrypt/ui/app.py --server.port=8501 --server.address=0.0.0.0