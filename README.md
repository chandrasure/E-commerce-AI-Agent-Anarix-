# 🛍️ E-commerce AI Agent – Anarix

Anarix is an AI-powered agent that answers natural language questions about e-commerce data. It uses a Large Language Model (LLM) to convert user queries into SQL, fetches insights from structured product-level data, and responds through an API interface. It also supports visualizations and live streaming-style responses for a more interactive experience.

---

## 🚀 Project Features

- 🔍 **Natural Language Query Understanding**  
  Converts user questions into SQL queries using an LLM.

- 🗃️ **Structured E-commerce Dataset Access**  
  Handles data from:
  - Product-Level Ad Sales & Metrics
  - Product-Level Total Sales & Metrics
  - Product-Level Eligibility Table

- 📡 **Fast API Integration**  
  Receives questions via endpoints and returns clean, human-readable responses.

- 📊 **Interactive Visualizations** *(Bonus)*  
  Supports data plots using Plotly or Matplotlib.

- ⌨️ **Live Typing (Streaming) Response** *(Bonus)*  
  Simulates real-time AI interaction by streaming the response like a chat.

---

## 🧠 Tech Stack

| Component       | Tech Used                            |
|----------------|--------------------------------------|
| Language Model  | Local LLM (e.g., Llama3, Mistral) or Gemini 2.5 API |
| Backend         | Python, FastAPI                      |
| Database        | SQLite / PostgreSQL (via SQLAlchemy) |
| Visualizations  | Matplotlib / Plotly                  |
| Frontend        | Streamlit (for dashboard UI)         |
| API Testing     | Postman / curl                       |

---

## 📂 Dataset Overview

1. **Product-Level Ad Sales and Metrics**  
   - `date`, `item_id`, `ad_sales`, `impressions`, `ad_spend`, `clicks`, `units_sold`

2. **Product-Level Total Sales and Metrics**  
   - `date`, `item_id`, `total_sales`, `total_units_ordered`

3. **Product-Level Eligibility Table**  
   - `eligibility_datetime_utc`, `item_id`, `eligibility`, `message`

---

## 🔄 Workflow

1. Convert CSV datasets into SQL tables.
2. Receive user query through API.
3. LLM translates query → SQL.
4. Execute SQL on database.
5. Return results as:
   - Clean text
   - Charts (if applicable)
   - Streaming-style (if enabled)

---

## 📌 Example Questions

- **What is my total sales?**
- **Calculate the RoAS (Return on Ad Spend).**
- **Which product had the highest CPC?**

---

## ▶️ Demo Instructions

1. Clone this repo  
   `git clone https://github.com/your-username/E-commerce-AI-Agent-Anarix.git`

2. Install dependencies  
   `pip install -r requirements.txt`

3. Run backend server  
   `uvicorn main:app --reload`

4. Run Streamlit dashboard *(optional)*  
   `streamlit run dashboard.py`

5. Test with curl or Postman  
   ```bash
   curl -X POST http://localhost:8000/query \
   -H "Content-Type: application/json" \
   -d '{"question": "What is my total sales?"}'
