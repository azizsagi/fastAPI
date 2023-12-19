import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

#Connect with the database
def connect():
    return mysql.connector.connect(
        host = MYSQL_HOST,
        user = MYSQL_USER,
        password = MYSQL_PASSWORD,
        database = MYSQL_DATABASE
    )

# Add into user table
def add_user(name:str, email:str):
    conn = connect()
    cursor = conn.cursor()
    query = "INSERT INTO users SET name = %s, email = %s"
    values = (name,email)
    cursor.execute(query,values)
    conn.commit()
    conn.close()
    return cursor.lastrowid

# Fetch all users
def all_db_users():
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    records = cursor.fetchall()
    conn.close()
    return records