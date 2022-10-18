import mysql.connector

mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     password="password123"
    )

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mtgdatabase")
