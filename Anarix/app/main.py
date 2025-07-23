from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.llm_interface import question_to_sql
from app.db_query import execute_query, format_result
from app.visualize import generate_chart, chart_needed
import time

app = FastAPI(title="E-Commerce AI Agent", description="Ask questions about your e-commerce data.", version="1.0.0")

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "Welcome to the E-Commerce AI Agent API! Use /docs for interactive API."}

@app.post("/ask", tags=["Q&A"])
async def ask_question(q: Question):
    sql = await question_to_sql(q.question)
    result = execute_query(sql)
    answer = format_result(result)
    if chart_needed(q.question) and "rows" in result and result["rows"]:
        chart_path = generate_chart(result["rows"], q.question)
        return {"answer": answer, "chart": chart_path}
    return {"answer": answer}

def fake_streamer(answer):
    for word in answer.split():
        yield word + " "
        time.sleep(0.2)

@app.post("/ask-stream", tags=["Q&A"])
async def ask_stream(q: Question):
    sql = await question_to_sql(q.question)
    result = execute_query(sql)
    answer = format_result(result)
    return StreamingResponse(fake_streamer(answer), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True) 