import mysql.connector
import streamlit as st

@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_database"
    )
