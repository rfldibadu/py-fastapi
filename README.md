# 🧾 FastAPI Purchase Service

A simple FastAPI backend for managing purchase records and item pricing logic.

## 🛠 Features

- Create purchases with adjusted prices
- Apply additional costs and discounts proportionally
- Auto-calculate item-level prices
- In-memory data storage (no database yet)

## 📦 Tech Stack

- FastAPI
- Pydantic
- Python 3.13+

## 🚀 How to Run

```bash
uvicorn app.main:app --reload
