from db_connection import *


class GameUtil:

    def user_exists(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE did = %s ", (self,))
        row = cur.fetchone()
        cur.close()
        return True if row else False

    def user_get(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE did = %s ", (self,))
        row = cur.fetchone()
        cur.close()
        return row

    def user_create(self, discord_name, score=0, reactions_triggered=0):
        cur = conn.cursor()
        cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s)", (self, discord_name, score, reactions_triggered))
        print("Posted user to DB | {}: {}".format(self, discord_name))
        cur.close()

    def increment_score(self, score):
        cur = conn.cursor()
        cur.execute("UPDATE users SET score = score + %s WHERE did = %s", (score, self))
        cur.close()

    def reduce_score(self, score):
        cur = conn.cursor()
        cur.execute("UPDATE users SET score = score - %s WHERE did = %s", (score, self))
        cur.close()

    def multiply_score(self, score):
        cur = conn.cursor()
        cur.execute("UPDATE users SET score = score * %s WHERE did = %s", (score, self))
        cur.close()

    def increment_reaction_counter(self, score):
        cur = conn.cursor()
        cur.execute("UPDATE users SET reactions_triggered = reactions_triggered + %s WHERE did = %s", (score, self))
        cur.close()
