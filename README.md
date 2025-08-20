# 🛒 Amazon Scraping + AI Answer API

This project provides a backend service to scrape Amazon product data, store it in a PostgreSQL database with pgvector, and leverage LLM embeddings for semantic search and AI-powered product comparison.

It uses FastAPI for the web API, Ollama for local LLM inference, and Docker Compose for orchestration.  
If you have an NVIDIA GPU, the setup automatically detects it and enables GPU acceleration for faster AI responses.

---

## ✨ Features

- 🔍 Scrape Amazon product search results and single product pages.
- 📦 Persist products into PostgreSQL with vector embeddings.
- 🤖 AI-powered semantic search over products using embeddings.
- ⚖️ Intelligent product comparison via LLM (Ollama).
- 🚀 Dockerized deployment with optional GPU acceleration.

---

## ⚙️ Tech Stack

- **FastAPI** — Web API framework  
- **PostgreSQL + pgvector** — Vector similarity search  
- **Ollama** — Local LLM inference  
- **Docker & Docker Compose** — Containerized deployment  
- **SQLAlchemy** — ORM for database interaction  

---

## 📡 API Endpoints

### 🔗 Scraping

**POST /scrap/list_url**  
Scrape multiple products from an Amazon search page.

Example body:
```json
{
  "url": "https://www.amazon.com/s?k=computer",
  "total_pages": 2
}
```
✅ Returns a list of products scraped.

---

**POST /scrap/single_product**  
Scrape details from a single Amazon product page.

Example body:
```json
{
  "url": "https://www.amazon.com/.../dp/B0D4TZNPMX"
}
```
✅ Returns product details (title, price, description, etc.).

---

### 📦 Products

**GET /products/search?q=<text>**  
Perform a semantic search across products stored in the database.

Query params:  
- `q` → text to search semantically  

✅ Returns a ranked list of matching products with similarity scores.

---

**GET /products/compare_products?ids=1&ids=2&ids=3**  
Compare two or more products using AI analysis.

Query params:  
- `ids` → list of product IDs stored in DB  

❌ Requires at least 2 valid products.  
✅ Returns an AI-generated comparison of the selected products.

---

## 🐳 Deployment with Docker

### 1. Prerequisites
- Docker  
- Docker Compose  

If you have an NVIDIA GPU, install the NVIDIA container toolkit:
```bash
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

---

### 2. Start the services
```bash
docker-compose up --build
```

**Services started:**
- Ollama LLM → http://localhost:11434  
- API (FastAPI) → http://localhost:8000  
- Postgres (pgvector) → port 5432  

---

### 3. GPU Acceleration
On startup, the container checks if `nvidia-smi` is available.  

- If GPU is found → `OLLAMA_GPU=1` (faster inference).  
- Otherwise → falls back to CPU.  
