from db_connection import *


class ReactUtil:

    def get_reacts(self):
        msg = self.lower()
        cur = conn.cursor()
        cur.execute("select * from reactions where %s like '%%' || keyword || '%%'", (msg,))
        rows = cur.fetchall()
        cur.close()
        if rows:
            return rows
