import sqlite3

conn = sqlite3.connect('user4.db')
cursor = conn.cursor()

# Insert a test user (replace with your desired credentials)
cursor.execute("""
    INSERT INTO user4 (username, password, email, role, status, rolebase_gptname) 
    VALUES (?, ?, ?, ?, ?, ?)
""", ("Sameer", "Test123!", "sjejurkar@valueglobal.net", "Admin", "Active", "Select a Role & GPT"))

conn.commit()
conn.close()