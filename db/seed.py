from connection import get_connection
import json 

conn = get_connection()

def seed():
    drop_table("users")
    create_user_table()
    insert_user_info()

def drop_table(table_name):
    cursor = conn.cursor()
    drop = f"DROP TABLE IF EXISTS {table_name};"
    cursor.execute(drop)
    cursor.close()

def create_user_table():
    cursor = conn.cursor()
    users = """ CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL, 
    created_at TIMESTAMPTZ DEFAULT NOW()
    ); """
    cursor.execute(users)
    conn.commit()
    cursor.close()

def insert_user_info():
    cursor = conn.cursor()
    with open("./db/data/users.json") as file:
        users = json.load(file)

    for user in users:
        insert_statement = """ INSERT INTO users 
        (email, password, name) VALUES (%s,%s,%s); """
        cursor.execute(insert_statement,
                       (user["email"], user["password"],user["name"]))
    conn.commit()
    cursor.close()

seed()
conn.close()