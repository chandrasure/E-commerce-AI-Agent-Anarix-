import os
import httpx
from dotenv import load_dotenv
import re

load_dotenv()

LLM_MODE = os.getenv("LLM_MODE", "gemini")  # 'gemini' or 'local'
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY and LLM_MODE == "gemini":
    raise ValueError("GOOGLE_API_KEY is not set in .env!")

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key="
    + GOOGLE_API_KEY
    if GOOGLE_API_KEY else None
)

SCHEMA = '''
Tables:
- ad_sales_metrics(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
- total_sales_metrics(date, item_id, total_sales, total_units_ordered)
- eligibility_table(eligibility_datetime_utc, item_id, eligibility, message)
'''

def clean_sql(sql: str) -> str:
    sql = sql.strip()
    sql = re.sub(r"^```sql\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^```", "", sql)
    sql = re.sub(r"```$", "", sql)
    return sql.strip()

async def gemini_question_to_sql(question: str) -> str:
    prompt = f"""
You are a data analyst assistant.
{SCHEMA}
Task: Convert this question into a SQL query.
Question: {question}
"""
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(GEMINI_API_URL, json=data, headers=headers, timeout=30)
        resp.raise_for_status()
        sql = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        return sql.strip()

async def question_to_sql(question: str) -> str:
    if LLM_MODE == "gemini" and GOOGLE_API_KEY:
        sql = await gemini_question_to_sql(question)
        return clean_sql(sql)
    # Local LLM or fallback
    if "total sales" in question.lower():
        return "SELECT SUM(total_sales) FROM total_sales_metrics;"
    if "roas" in question.lower():
        return "SELECT ROUND(SUM(ad_sales) / NULLIF(SUM(ad_spend), 0), 2) as RoAS FROM ad_sales_metrics;"
    if "highest cpc" in question.lower():
        return "SELECT item_id, ROUND(ad_spend / NULLIF(clicks, 0), 2) as CPC FROM ad_sales_metrics ORDER BY CPC DESC LIMIT 1;"
    return "SELECT 1;" 