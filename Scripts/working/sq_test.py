import sqlite3 as sq3

# Connect to the database
connection = sq3.connect('sqlite.db')

# Create cursor
cursor = connection.cursor()

# Get the structure of the table
cursor.execute("SELECT * FROM archive")

# Fetch the all table results
info = cursor.fetchall()

for row in info:
    print(row)

# Close cursor and connection
cursor.close()
connection.close()