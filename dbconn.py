import psycopg2
import constants as cons

try:
    conn = psycopg2.connect(cons.DATABASE_URL, sslmode='require')
    conn.autocommit = True
except:
    print("Cannot connect to db")
