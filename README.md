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
- **Caching**: Redis
- **External API**: [CoinGecko API](https://www.coingecko.com/en/api/documentation)
- **Containerization**: Docker, Docker Compose

---

## 📦 Setup (Docker)

1. **Clone the repository**
   ```bash
   git clone https://github.com/calmrat/qrypto.git
   cd qrypto


## 🌞 Setup (uv)
1. **Clone the repository**
   ```bash
   git clone https://github.com/calmrat/qrypto.git
   cd qrypto
   uv sync
