import streamlit as st
from db import get_connection

st.title("🏈 Team Directory")

# Prompt for connection
conn = get_connection()

if not conn:
    st.warning("Please enter your MySQL password and database name to connect.")
    st.stop()

try:
    query = "SELECT TeamInitial, TeamName, City FROM teams ORDER BY TeamInitial"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    if rows:
        st.dataframe([dict(zip(columns, row)) for row in rows])
    else:
        st.info("No teams found.")

except Exception as e:
    st.error(f"Error retrieving team data: {e}")
