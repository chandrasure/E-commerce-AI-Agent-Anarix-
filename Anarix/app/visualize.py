import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

def chart_needed(question: str) -> bool:
    keywords = ["show", "visualize", "chart", "plot", "graph"]
    return any(k in question.lower() for k in keywords)

def generate_chart(data, question: str) -> str:
    """
    Generate a chart from SQL result rows. Auto-detects columns and chart type.
    """
    # Try to infer columns
    if not data or not isinstance(data, list) or not data[0]:
        return None
    # Heuristic: if two columns, bar chart; if time series, line chart
    if len(data[0]) == 2:
        df = pd.DataFrame(data, columns=["x", "y"])
        if "over time" in question.lower() or "date" in question.lower():
            chart_type = "line"
        else:
            chart_type = "bar"
    else:
        # Fallback: plot first two columns
        df = pd.DataFrame(data)
        df = df.iloc[:, :2]
        df.columns = ["x", "y"]
        chart_type = "bar"
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    if chart_type == "line":
        ax = sns.lineplot(x="x", y="y", data=df, marker="o")
    else:
        ax = sns.barplot(x="x", y="y", data=df, palette="coolwarm")
    plt.title("Chart", fontsize=16, color="#333333")
    plt.xlabel(df.columns[0], fontsize=12)
    plt.ylabel(df.columns[1], fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart_path = "output.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path 

def clean_sql(sql: str) -> str:
    sql = sql.strip()
    sql = re.sub(r"^```sql\\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^```", "", sql)
    sql = re.sub(r"```$", "", sql)
    return sql.strip() 