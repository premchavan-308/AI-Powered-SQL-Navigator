import streamlit as st
import pandas as pd
import mysql.connector
import google.generativeai as genai

# 1. Setup Gemini AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets["MYSQL_HOST"],
        user=st.secrets["MYSQL_USER"],
        password=st.secrets["MYSQL_PASSWORD"],
        database=st.secrets["MYSQL_DATABASE"],
        port=st.secrets["MYSQL_PORT"]
    )

def generate_sql_from_ai(user_query):
    prompt = f"Convert this natural language request into a valid MySQL query: '{user_query}'. Only return the raw SQL string."
    response = model.generate_content(prompt)
    return response.text.replace("```sql", "").replace("```", "").strip()

# Page Configuration
st.set_page_config(page_title="AI SQL Navigator", page_icon="⚡", layout="wide")

st.title("⚡ AI-Powered SQL Navigator")
st.markdown("---")

# Session Management
if "sql_query" not in st.session_state: st.session_state.sql_query = None
if "results" not in st.session_state: st.session_state.results = None

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2721/2721990.png", width=100)
    if st.button("🔄 Reset Application"):
        st.session_state.clear()
        st.rerun()

# Layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 📝 Request Builder")
    user_query = st.text_area("What do you want to see?", height=100)
    
    if st.button("✨ Generate SQL Query"):
        if user_query:
            st.session_state.sql_query = generate_sql_from_ai(user_query)
        else:
            st.warning("Please enter a query.")

    if st.session_state.sql_query:
        st.code(st.session_state.sql_query, language="sql")
        if st.button("🚀 Run Execution"):
            try:
                conn = get_db_connection()
                st.session_state.results = pd.read_sql(st.session_state.sql_query, conn)
                conn.close()
            except Exception as e:
                st.error(f"Execution Error: {e}")

with col2:
    st.markdown("### 📊 Live Data Preview")
    if isinstance(st.session_state.results, pd.DataFrame):
        st.dataframe(st.session_state.results, use_container_width=True)
        csv = st.session_state.results.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, "results.csv", "text/csv")
    else:
        st.info("Execute a query to see results.")
