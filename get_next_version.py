import re
import sqlite3

def is_strong_password(password):
    return (len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'\d', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

#def get_next_version():
    #with sqlite3.connect('autogpt1.db') as conn:
        #cur = conn.cursor()
        #cur.execute("SELECT version FROM autogpt1 ORDER BY id DESC LIMIT 1")
        #last_version = cur.fetchone()
        #if not last_version or not last_version[0]:
            #return "v1.0.0"
        #version_number = int(last_version[0].split('.')[0][1:])
        #return f"v{version_number + 1}.0.0"
