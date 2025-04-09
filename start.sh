#!/bin/bash
# Activate virtual environment

which uvicorn
which streamlit

pwd
ls -la

uv pip install --system -e .

#uv pip list
#printenv

echo Initializing database
uv run init_db
echo DONE

echo Pulling tokens
uv run pull_tokens
echo DONE

uvicorn qrypt.main:app --host 0.0.0.0 --port 8000 &

streamlit run src/qrypt/ui/app.py --server.port=8501 --server.address=0.0.0.0