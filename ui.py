import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(page_title="AI SQL Navigator", page_icon="⚡", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 5px; height: 3em; 
        background-color: #007bff; color: white; border: none;
        font-weight: bold;
    }
    .stButton>button:hover { background-color: #0056b3; }
    .css-1544g2n { padding: 2rem; border-radius: 10px; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ AI-Powered SQL Navigator")
st.subheader("Turn natural language into database insights instantly.")
st.markdown("---")

# Session Management
if "sql_query" not in st.session_state: st.session_state.sql_query = None
if "results" not in st.session_state: st.session_state.results = None

# Sidebar Controls
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2721/2721990.png", width=100)
    st.header("App Settings")
    if st.button("🔄 Reset Application"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()
    st.markdown("---")
    st.info("System Status: **Connected** ✅")

# Layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 📝 Request Builder")
    user_query = st.text_area("What do you want to see?", placeholder="e.g., Get me the top 5 highest paid employees...", height=100)
    
    if st.button("✨ Generate SQL Query"):
        if user_query:
            response = requests.post("http://127.0.0.1:8000/generate_sql/", json={"query": user_query})
            if response.status_code == 200:
                st.session_state.sql_query = response.json().get("sql")
            else:
                st.error("Failed to communicate with AI Engine.")

    if st.session_state.sql_query:
        st.markdown("#### 💻 Generated SQL:")
        st.code(st.session_state.sql_query, language="sql")
        
        if st.button("🚀 Run Execution"):
            payload = {"sql": st.session_state.sql_query}
            response = requests.post("http://127.0.0.1:8000/execute_sql/", json=payload)
            if response.status_code == 200:
                data = response.json()
                st.session_state.results = data.get("results", [])
            else:
                st.error("Execution failed.")

with col2:
    st.markdown("### 📊 Live Data Preview")
    if st.session_state.results:
        df = pd.DataFrame(st.session_state.results)
        st.dataframe(df, use_container_width=True, height=400)
        
        if st.session_state.results:
            df = pd.DataFrame(st.session_state.results)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Data as CSV",
                data=csv,
                file_name='query_results.csv',
                mime='text/csv',
            )
    else:
        st.warning("No data loaded. Execute a query to see results here.")

st.markdown("---")
st.caption("Powered by Gemini 3.5 & FastAPI | Built for speed")