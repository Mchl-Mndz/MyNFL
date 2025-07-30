import streamlit as st
from db import get_connection

st.title("🎓 College Alumni Viewer")

# Connect to the database
conn = get_connection()

if not conn:
    st.warning("Please connect to the database using the sidebar.")
    st.stop()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT `College/Univ` FROM players p JOIN college c ON p.ID = c.ID WHERE `College/Univ` IS NOT NULL ORDER BY `College/Univ`")
    colleges = [row[0] for row in cursor.fetchall()]

    if not colleges:
        st.info("No colleges found in the database.")
        st.stop()

    selected_college = st.selectbox("Select a college or university:", colleges)

    cursor.execute("SELECT DISTINCT Player FROM players p JOIN college c ON p.ID = c.ID WHERE `College/Univ` = %s ORDER BY Player", (selected_college,))
    players = cursor.fetchall()
    player_columns = [desc[0] for desc in cursor.description]

    if players:
        st.subheader(f"Players from {selected_college}")
        st.dataframe([dict(zip(player_columns, row)) for row in players])
    else:
        st.info(f"No players found from {selected_college}.")

except Exception as e:
    st.error(f"Error: {e}")
