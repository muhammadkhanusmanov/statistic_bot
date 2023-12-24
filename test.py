import sqlite3
import json

# a = json.loads(open('lists.json').read())

cnt = sqlite3.connect('data.db')
cr = cnt.cursor()
k=1


commands=f"""
INSERT INTO Admins VALUES (
1,
"5032606464",
"0",
1
)
"""

cr.execute(commands)
cnt.commit()
