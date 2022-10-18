import json

from mtgsdk import Card
import mysql.connector





mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     password="password123",
     database="mtgdatabase"
    )

mycursor = mydb.cursor()

sql = 'INSERT INTO cards (multiverseid, name, colors, cmc, supertypes, types, subtypes, power, toughness, series) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
try:
    for k in range(1000):
        allCards = []
        print(k)
        cards = Card.where(page=k).where(pagesize=1000).all()
        for i in cards:
            multiverseid = ""
            for j in i.multiverseid:
                multiverseid = str(j) + " " + multiverseid
            colors = ""
            for j in i.colors:
                colors = str(j) + " " + colors
            supertypes = ""
            for j in i.supertypes:
                supertypes = str(j) + " " + supertypes
            subtypes = ""
            for j in i.subtypes:
                subtypes = str(j) + " " + subtypes
            types = ""
            for j in i.types:
                types = str(j) + " " + types

            card = (i.multiverseid, i.name, colors, i.cmc, supertypes, types, subtypes, i.power, i.toughness, i.set)
            allCards.append(card)
            print(card)
        mycursor.executemany(sql, allCards)
        mydb.commit()

except mysql.connector.Error as error:
    print("Failed to insert record".format(error))

finally:
    mycursor.executemany(sql, allCards)
    mydb.commit()


