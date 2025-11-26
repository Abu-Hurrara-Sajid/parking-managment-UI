import pyodbc
# print("Pyodbc installed")
#now create connection to sql server
conn=pyodbc.connect(
      'DRIVER={ODBC DRIVER 17 FOR SQL SERVER};'
      'SERVER={DESKTOP-KUT14B4\SQLEXPRESS};'
      'DATABASE=master;'
      'TRUSTED_CONNECTION=YES;',
    #   autocommit=True
     

)
cursor=conn.cursor()
print("Connection created successfully")
cursor.execute("IF DB_ID('Harrydb_db')IS NULL CREATE DATABASE Harrydb_db;")
conn.commit()
print("Database created")