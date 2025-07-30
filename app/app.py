import streamlit as st

st.set_page_config(page_title="MyNFL", layout="centered")

st.title("🏟️ MyNFL Home")

st.markdown("""
Welcome! Choose an option below:
- [Game Results](./Game_Results)
- [List of Teams](./Teams_List)
- [Interesting Query Tool](./Queries)
- [Explore active NCAA Alumni](./College_Alumni)
""")
