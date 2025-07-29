import mysql.connector
import streamlit as st

def get_connection():
    # If we already connected, return the stored connection
    if "mysql_conn" in st.session_state:
        return st.session_state["mysql_conn"]

    # If not yet connected, show login form
    with st.sidebar:
        st.header("🔐 Connect to MySQL")

        if "mysql_password" not in st.session_state:
            st.session_state["mysql_password"] = ""
        if "mysql_db" not in st.session_state:
            st.session_state["mysql_db"] = ""

        password = st.text_input("MySQL Password", type="password", key="mysql_password")
        database = st.text_input("Database Name", key="mysql_db")
        connect_button = st.button("Connect")

        if connect_button and password and database:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password=password,
                    database=database
                )
                st.session_state["mysql_conn"] = conn
                st.success(f"Connected to `{database}`!")
            except mysql.connector.Error as err:
                st.error(f"Connection failed: {err}")

    return st.session_state.get("mysql_conn", None)
