# E-Commerce AI Agent

## Overview
A modular AI-powered agent that answers e-commerce data questions using natural language, SQL, and visualizations. Features:
- RESTful API for user questions
- LLM-powered SQL translation (Gemini API or local LLM)
- SQLite backend
- Data visualization (charts)
- Streamed/live answer support

## Project Structure
```
ecommerce_ai_agent/
│
├── data/
│   ├── ad_sales.csv
│   ├── total_sales.csv
│   └── eligibility.csv
│
├── db/
│   └── ecommerce.db
│
├── app/
│   ├── main.py            # FastAPI app
│   ├── llm_interface.py   # LLM prompt and SQL conversion
│   ├── db_query.py        # SQL execution
│   ├── visualize.py       # Plotly/matplotlib charting
│   ├── data_ingest.py     # Data ingestion
│   └── __init__.py
│
├── demo/
│   └── demo_video.mp4
│
├── requirements.txt
├── README.md
└── .env
```

## Setup
1. Place your CSVs in `data/`.
2. Run the app to ingest data and start the API.
3. Use `/ask` or `/ask-stream` endpoints to query.

## Data Ingestion

1. Place your CSV files in the `data/` directory.
2. Run the following command to ingest data and create the SQLite database:

```bash
python app/data_ingest.py
```

## LLM Integration

- By default, the agent uses Google Gemini API for SQL translation.
- Set your API key and mode in `.env`:

```
GOOGLE_API_KEY=your_google_api_key
LLM_MODE=gemini  # or 'local' for local LLM integration
DB_PATH=db/ecommerce.db
```

- To use a local LLM (Ollama, LM Studio, etc.), set `LLM_MODE=local` and implement the local LLM call in `llm_interface.py`.

## Running the API

Start the FastAPI server with:

```bash
python -m uvicorn app.main:app --reload
```

## API Usage

- **POST /ask**: Submit a question in JSON: `{ "question": "What is my total sales?" }`
- **POST /ask-stream**: Same as above, but streams the answer word by word.

Example using `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"question": "What is my total sales?"}'
```

If the question requests a chart, the response will include a path to the generated image.

## Features
- Modular codebase
- LLM-to-SQL translation (Gemini/local)
- Data visualization
- Streaming answers

## Environment
- Python 3.9+
- FastAPI
- SQLite
- Pandas, Plotly/Matplotlib

## Usage
See `app/main.py` for API usage examples. 

---

## 1. **Common Error Sources**

### **A. Asynchronous LLM Call in Synchronous Context**
- Your `llm_interface.py` uses `asyncio.run(gemini_question_to_sql(question))` inside a synchronous function (`question_to_sql`). If `/ask` or `/ask-stream` is called multiple times, or if FastAPI is running in an async context, this can cause errors like:
  - `RuntimeError: asyncio.run() cannot be called from a running event loop`
  - Or, the server may hang or crash.

**Solution:**  
- Make `question_to_sql` an `async def` and always `await` it in your FastAPI endpoints.

---

### **B. Missing or Invalid API Key**
- If your `.env` is not loaded, or the API key is missing/invalid, you may get HTTP 401/403 errors or `KeyError`/`NoneType` errors.

**Solution:**  
- Double-check your `.env` file is in the project root and contains:
  ```
  GOOGLE_API_KEY=AIzaSyA9Wtm_n81BV4UqfgGCWpUn4_D53NVhBaM
  LLM_MODE=gemini
  DB_PATH=db/ecommerce.db
  ```
- Restart your terminal after editing `.env`.

---

### **C. HTTPX/Network Errors**
- If the Gemini API is unreachable, you may see `httpx.ConnectError`, `TimeoutError`, or similar.

---

### **D. SQL/Database Errors**
- If the SQL generated is invalid, or the DB is missing, you may see SQLite errors.

---

## 2. **How to Fix (Step-by-Step)**

### **Step 1: Refactor LLM Call to be Fully Async**
- In `llm_interface.py`:
  ```python
  async def question_to_sql(question: str) -> str:
      if LLM_MODE == "gemini" and GOOGLE_API_KEY:
          return await gemini_question_to_sql(question)
      # ...rest as before...
  ```
- In `main.py`, update endpoint calls:
  ```python
  @app.post("/ask", tags=["Q&A"])
  async def ask_question(q: Question):
      sql = await question_to_sql(q.question)
      result = execute_query(sql)
      answer = format_result(result)
      # ...rest as before...
  ```
  (Do the same for `/ask-stream`.)

---

### **Step 2: Check .env and API Key**
- Make sure `.env` is in your project root and is correct.
- If you change `.env`, restart your terminal and server.

---

### **Step 3: Check Terminal Output**
- Look for the **first error** in the stack trace.  
- If it's an import, async, or HTTP error, follow the above fixes.

---

### **Step 4: Share the Error**
- If you still get errors, **copy and paste the full error message or stack trace** here.  
- This will help me give you a precise fix.

---

## **Summary Table**

| Error Type                | Likely Cause                        | Fix                                      |
|---------------------------|-------------------------------------|------------------------------------------|
| asyncio.run() error       | Mixing sync/async                   | Make LLM call fully async                |
| KeyError/NoneType         | .env not loaded/API key missing     | Check .env, restart terminal             |
| HTTPX/Timeout             | Network/API issue                   | Check API key, network, Gemini status    |
| SQLite/DB error           | Bad SQL or missing DB               | Check SQL, run data_ingest.py            |

---

**If you paste the exact error(s) you see, I can give you a line-by-line fix!**  
Would you like me to generate the corrected async code for you? 