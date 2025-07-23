import streamlit as st
import requests
import time
from PIL import Image
import re

API_URL = "http://localhost:8000"

st.set_page_config(page_title="E-Commerce AI Agent", page_icon="🛒", layout="wide")

# Custom CSS for glassmorphism, fonts, buttons, stat cards, etc.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Open+Sans:wght@400;600&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Poppins', 'Open Sans', Arial, sans-serif !important;
        background: linear-gradient(120deg, #F8F9FA 0%, #EDEDED 100%);
    }
    .glass-card {
        background: rgba(255,255,255,0.7);
        box-shadow: 0px 4px 24px rgba(0,0,0,0.10);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(8px);
    }
    .stat-card {
        background: rgba(255,255,255,0.85);
        box-shadow: 0px 4px 12px rgba(0,0,0,0.10);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        margin: 1.5rem 0;
        text-align: center;
    }
    .stat-label {
        font-size: 18px;
        color: #888;
    }
    .stat-value {
        font-size: 40px;
        font-weight: bold;
        color: #2d6a4f;
    }
    .gradient-btn {
        background: linear-gradient(to right, #667eea, #764ba2);
        color: #fff !important;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 18px;
        font-weight: 600;
        box-shadow: 0 2px 8px #e0e0e0;
        transition: box-shadow 0.2s;
    }
    .gradient-btn:hover {
        box-shadow: 0 4px 16px #b39ddb;
        filter: brightness(1.05);
    }
    .centered { text-align: center; }
    .subtitle { font-size: 18px; color: #666; }
    .footer { text-align: center; color: #888; font-size: 14px; margin-top: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Hero section with title, subtitle, and illustration
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(
        """
        <div class="centered">
            <span style="font-size:48px;">🛒</span>
            <p class="title" style="font-size:36px;font-weight:bold;color:#333333;font-family:'Poppins'">E-Commerce AI Agent</p>
            <p class="subtitle" style="font-size:18px;color:#666;">Ask anything about your product performance metrics</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
# with col2:
    # st.image("https://undraw.co/api/illustrations/undraw_online_stats_0g94.svg", use_container_width=True)

# Sidebar: dataset summary and filters
with st.sidebar:
    st.markdown("## 📊 Dataset Summary")
    st.markdown("- Ad Sales: ad_sales.csv")
    st.markdown("- Total Sales: total_sales.csv")
    st.markdown("- Eligibility: eligibility.csv")
    st.markdown("---")
    st.markdown("**Try a sample question:**")
    example = st.selectbox(
        "Examples:",
        [
            "What is my total sales?",
            "Calculate the RoAS (Return on Ad Spend).",
            "Which product had the highest CPC?",
            "Show ad sales over time",
            "Visualize product-wise CPC",
            "Top products by impressions"
        ],
        key="example_select"
    )
    st.markdown("---")
    st.markdown("[GitHub Repo](https://github.com/) · Powered by Streamlit + Gemini")

# Main input area
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

with st.form("question_form"):
    st.markdown(
        '<span style="font-size:16px;color:#555;font-family:Open Sans;">Enter your question:</span> '
        '<span title="Try asking about sales, RoAS, CPC, trends, or product performance!" style="cursor:help;">❓</span>',
        unsafe_allow_html=True,
    )
    question = st.text_input(
        "Your Question",
        value=example,
        key="question_input",
        label_visibility="collapsed"
    )
    submit = st.form_submit_button(
        "Ask Question",
        use_container_width=True,
        help="Submit your question to the AI agent."
    )

st.markdown('</div>', unsafe_allow_html=True)

# Helper to extract number for stat card
def extract_number(answer):
    match = re.search(r"([-+]?[0-9]*\.?[0-9]+)", answer.replace(',', ''))
    if match:
        return float(match.group(1))
    return None

if submit and question:
    with st.spinner("Thinking..."):
        try:
            resp = requests.post(f"{API_URL}/ask", json={"question": question}, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            answer = data.get("answer", "No answer returned.")
            chart_path = data.get("chart")
        except Exception as e:
            answer = f"Error: {e}"
            chart_path = None

    if answer:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Answer:")
        value = extract_number(answer)
        if value is not None and ("total_sales" in answer or "RoAS" in answer or "CPC" in answer):
            st.markdown(
                f"""
                <div class="stat-card">
                    <span class="stat-label">Result</span><br>
                    <span class="stat-value">{value:,.2f}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Live typing effect for non-stat answers
            placeholder = st.empty()
            displayed = ""
            for word in answer.split():
                displayed += word + " "
                placeholder.markdown(
                    f"<div style='font-family:Open Sans,Arial Rounded MT,Roboto;font-size:20px;color:#333333;background:rgba(255,255,255,0.7);padding:10px;border-radius:8px'>{displayed}</div>",
                    unsafe_allow_html=True,
                )
                time.sleep(0.04)
        st.markdown('</div>', unsafe_allow_html=True)

    if chart_path:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Visualization:")
        try:
            image = Image.open(chart_path)
            st.image(image, use_container_width=True, caption="Chart")
        except Exception as e:
            st.error(f"Could not load chart: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        <hr style="border:0;border-top:1px solid #eee;"/>
        <span>Made with ❤️ by Chandra Kishore · <a href="https://github.com/" target="_blank">GitHub</a> · Powered by Streamlit + Gemini</span>
    </div>
    """,
    unsafe_allow_html=True,
) 