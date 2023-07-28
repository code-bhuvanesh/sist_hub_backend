import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Delete all rows from table
c.execute('DELETE FROM api_post;',);

print('We have deleted', c.rowcount, 'records from the table.')

# Commit the changes to db			
conn.commit()
# Close the connection
conn.close()