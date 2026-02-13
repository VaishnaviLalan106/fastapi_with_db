# 🛠 FastAPI Backend for AI Chat App

This repository contains the **backend API** for the AI Chat application, built with **FastAPI** and connected to a database to support authentication, chat history, and AI interactions.

---

## 🚀 Live Backend URL

*(https://fastapi-with-db-2-jnyu.onrender.com)*

---

## 🧠 Features

- 🚪 User Authentication (login/signup, JWT)
- 📚 Database-backed storage for users and chats
- 🗂 CRUD operations for managing chat history
- 🚀 Clean REST API using FastAPI
- 🧪 Built-in API documentation via OpenAPI/Swagger
- 🧰 Utility scripts for DB checks and management

---

## 💻 Tech Stack

- **Python**  
- **FastAPI** – high-performance API framework  
- **SQLAlchemy / ORM** – database integration  
- **SQLite (or your chosen DB)** for persistence  
- **Uvicorn** – ASGI server  
- **Dependency management** via `requirements.txt`

---
## 🛠 Installation & Running Locally

1. **Clone this repository**
   git clone https://github.com/VaishnaviLalan106/fastapi_with_db.git
   cd fastapi_with_db
2. **Create a virtual environment**
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
3. **Install dependencies**
   pip install -r requirements.txt
4. **Run the API**
   uvicorn main:app --reload

---

## 📦 Environment Variables
Create a .env file if using environment config (optional):

DATABASE_URL=sqlite:///test.db
GITHUB_TOKEN=your_github_token

