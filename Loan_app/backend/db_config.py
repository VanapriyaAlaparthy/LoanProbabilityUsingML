# backend/db_config.py
import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="loan_db",
        user="postgres",
        password="123456789"   # <- replace with your actual password
    )
