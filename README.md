# 🪙 Qrypto - A Crypto Records Manager UI 🚀

A containerized web application for managing cryptocurrency records using FastAPI, Streamlit, PostgreSQL, Redis, and the CoinGecko API. 
---

## 📻 Features

- CRUD API for crypto records
- CoinGecko API integration for symbol verification and metadata
- Auto-refresh of stale data
- Streamlit-based frontend UI
- Redis caching
- Dockerized with PostgreSQL and Redis

---

## 🛠️ Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: Streamlit
- **Caching**: Local JSON
- **External API**: [CoinGecko API](https://www.coingecko.com/en/api/documentation)
- **Containerization**: Docker

---

## 📦 Setup (Production with Docker)

1. **Clone the repository and Update .env**
   ```bash
   git clone https://github.com/calmrat/krypto-explorer
   cd krypto-explorer
   
   mv env-example .env
   # Update
   # CoinGecko Setup
   
   # # Coingecko API Key
   # Option A) Demo user with API key (recommended)
   KE_COINGECKO_API_DEMO_USER=true
   KE_COINGECKO_API_KEY=**YOUR_KEY_HERE**

   # Option B)
   # No API key (should work, but no guarantees)
   KE_COINGECKO_API_DEMO_USER=false
   KE_COINGECKO_API_KEY=

   # Database 
   # Option A) # Default - SQLite
   KE_DATABSE_URL=sqlite:///./crypt.db

   # Option B) Postgresql
   KE_DATABASE_USERNAME=**USERNAME**
   KE_DATABASE_PASSWORD=**PASSWORD**
   KE_DATABASE_NAME=qrypto
   KE_DATABASE_HOST=0.0.0.0
   KE_DATABASE_PORT=5432
   ```

2. **Build and start the Docker containers**
   ```bash
   docker compose build
   docker compose run --rm test
   docker compose up
   ```

3. **Access the application**
   - The backend API will be available at `http://localhost:8000`.
   - The frontend UI will be available at `http://localhost:8501`.

4. **Stop the containers**
   ```bash
   docker-compose down
   ```

---

## 🌞 Setup (Development with Virtual Environment + PIP)

1. **Clone the repository**
   ```bash
   git clone https://github.com/calmrat/qrypto.git
   cd qrypto
   ```

2. **Install uv, Create a virtual environment**
   ```bash
   
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv venv .venv
   source .venv/bin/activate
   uv python install 3.13
   ```

3. **Install dependencies**
   ```bash
   uv sync
   uv pip install -r pyproject.toml
   ```

4. **Run the backend API**
   ```bash
   uvicorn src.qrypt.main:app --reload
   ```

5. **Run the frontend UI**
   ```bash
   streamlit run src/qrypt/ui/app.py
   ```

6. **Access the application**
   - The backend API will be available at `http://localhost:8000`.
   - The frontend UI will be available at `http://localhost:8501`.
