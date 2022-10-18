import mysql.connector

mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     password="password123",
     database="mtgdatabase"
    )

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE combos ("
                 "comboCardId INT,"
                 "FOREIGN KEY (comboCardId) references cards(id),"
                 "comboCard2Id INT,"
                 "FOREIGN KEY (comboCard2Id) references cards(id),"
                 "CHECK (comboCardId <= comboCard2Id))")
#put some constraint on the DB to ensure duplicates do not happen
#e.g have lower ID card is card 1 then higher ID card is card 2