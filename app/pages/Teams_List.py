import streamlit as st
from db import get_connection
import pandas as pd

st.title("⚽ List of Teams")

conn = get_connection()
query = "SELECT TeamInitial, TeamName, City FROM teams ORDER BY TeamInitial"
df = pd.read_sql(query, conn)

st.dataframe(df)
