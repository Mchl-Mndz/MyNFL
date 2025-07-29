import streamlit as st

st.set_page_config(page_title="Sports Dashboard", layout="centered")

st.title("🏟️ Sports Dashboard Home")

st.markdown("""
Welcome! Choose an option below:
- [Game Results](./Game_Results)
- [List of Teams](./Teams_List)
- [Interesting Query Tool](./Queries)
""")
