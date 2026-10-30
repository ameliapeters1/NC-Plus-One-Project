from db.connection import get_connection
from auth.passwords import get_secret

def get_user(email):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s",
                            (email,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], 
                "email": row[1],
                "password_hash": row[2],
                "name":row[3],}

