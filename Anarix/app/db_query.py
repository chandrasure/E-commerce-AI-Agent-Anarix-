import sqlite3
import os

def get_db_connection():
    db_path = os.getenv("DB_PATH", "db/ecommerce.db")
    conn = sqlite3.connect(db_path)
    return conn

def execute_query(sql: str):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description] if cur.description else []
        conn.close()
        return {"columns": columns, "rows": rows}
    except Exception as e:
        conn.close()
        return {"error": str(e)}

def format_result(result) -> str:
    if "error" in result:
        return f"Error: {result['error']}"
    if not result["rows"]:
        return "No results found."
    # Format as table
    lines = []
    if result["columns"]:
        lines.append(" | ".join(result["columns"]))
        lines.append("-|-" * len(result["columns"]))
    for row in result["rows"]:
        lines.append(" | ".join(str(x) for x in row))
    return "\n".join(lines) 