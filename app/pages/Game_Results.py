import streamlit as st
from db import get_connection
import pandas as pd

st.title("📊 Game Results")

conn = get_connection()
query = "SELECT gameID, awayTeam, homeTeam, awayScore, homeScore, date FROM games ORDER BY date DESC"
df = pd.read_sql(query, conn)

st.dataframe(df)
