import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn.autocommit = True
except:
    print("Cannot connect to db")

