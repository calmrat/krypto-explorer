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

1. **Clone the repository**
   ```bash
   git clone https://github.com/calmrat/krypto-explorer
   cd krypto-explorer
   ```

2. **Build and start the Docker containers**
   ```bash
   docker compose build
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

## 🌞 Setup (Development with Virtual Environment)

1. **Clone the repository**
   ```bash
   git clone https://github.com/calmrat/qrypto.git
   cd qrypto
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend API**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Run the frontend UI**
   ```bash
   streamlit run app/frontend.py
   ```

6. **Access the application**
   - The backend API will be available at `http://localhost:8000`.
   - The frontend UI will be available at `http://localhost:8501`.
