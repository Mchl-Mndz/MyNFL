import streamlit as st
import pandas as pd
from db import get_connection  

st.title("📊 Game Results")

conn = get_connection()

if conn:
    try:
        query = """
            SELECT gameID, awayTeam, homeTeam, awayScore, homeScore, date
            FROM games
            ORDER BY date DESC
        """
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        st.dataframe([dict(zip(columns, row)) for row in rows])

    except Exception as e:
        st.error(f"Failed to execute query: {e}")
else:
    st.warning("Please enter your MySQL password and database name to connect.")