import mysql.connector

mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     password="password123",
     database="mtgdatabase"
    )

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE cards (id INT AUTO_INCREMENT PRIMARY KEY,"
                 "multiverseid INT, "
                 "name VARCHAR(255), colors VARCHAR(255), cmc FLOAT, "
                 "supertypes VARCHAR(255), types VARCHAR(255), subtypes VARCHAR(255), "
                 "power VARCHAR(255), toughness VARCHAR(255), series VARCHAR(255))")

