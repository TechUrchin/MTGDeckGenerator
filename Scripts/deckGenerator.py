from random import randrange

import mysql.connector
from fitnessFunction import *

mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     password="password123",
     database="mtgdatabase"
    )

mycursor = mydb.cursor()


class DeckGenerator():

    def __init__(self):
        self.i = "i"

    #TODO: Allow a deck to be loaded into the deck generator
    def loadDecks(self):
        print("Decks loaded")

    #TODO: Prepare the deck so that its in the same format as other decks and get all of a card's info e.g (id: x, cmc: 3....)
    def prepDecks(self):
        print("Decks prepped")

    #TODO: Multiple Colours to be selected
    def gatherCards(self, color):
        #Gather the cards for a deck and put into a list
        sql = ("SELECT * from cards where colors = '%s' AND types != 'Land ' ORDER BY RAND()  LIMIT 40") % (color)
        mycursor.execute(sql)
        c = mycursor.fetchall()
        return (c)

    def getCard(self, card):
        sql = ("SELECT * from cards where id = '%s' LIMIT 1") % (card)
        mycursor.execute(sql)
        card = mycursor.fetchall()
        return card[0] #returns the tuple outside of a list

    def getRandomCard(self, color):
        sql = ("SELECT * from cards where colors = '%s' AND types != 'Land ' ORDER BY RAND()  LIMIT 1") % (color)
        mycursor.execute(sql)
        card = mycursor.fetchall()
        return card[0] #returns the tuple outside of a list


    def gatherComboList(self, cardIds):
        #Gather all combo cards and put into a list
        comboList = []
        cardIds = tuple(cardIds)
        sql = "SELECT * from combos where comboCardId in {} OR comboCard2Id in {}".format(cardIds, cardIds)
        mycursor.execute(sql)
        comboList = mycursor.fetchall()
        return comboList


    def getComboCard(self, comboCards):
        randomIndex = randrange(len(comboCards))
        comboCard = comboCards[randomIndex] #get tuple from list
        comboCard0 = comboCard[0]
        comboCard1 = comboCard[1] #get card ID from tuple
        return comboCard0, comboCard1

    def getComboListFromDeck(self, cardIds, comboCards):
        deckCombos = []
        for combo in comboCards:
            comboCard1 = combo[0]
            comboCard2 = combo[1]
            if comboCard1 in cardIds and comboCard2 in cardIds:
                deckCombos.append(combo)

        return deckCombos

    def extractCardId(self, deck):
        cardIds = []
        for card in deck:
            cardIds.append(card[0])
        return cardIds

    def comboCheck(self, deck, combos, cardIds):
        if len(combos) != 0:
            comboCard0, comboCard1 = self.getComboCard(combos)  # returns combo card id

            existingComboCard = ""
            chosenComboCard = ""
            for id in cardIds:
                if id == comboCard0:
                    existingComboCard = comboCard0
                    chosenComboCard = comboCard1
                    break
                elif id == comboCard1:
                    existingComboCard = comboCard1
                    chosenComboCard = comboCard0
                    break

            chosenComboCard = self.getCard(chosenComboCard)  # returns combo card (all values)
            deck.append(chosenComboCard)

            if len(deck) > 40:
                chosenCardToDelete = None
                for card in deck:
                    if card[0] == existingComboCard or card[0] == chosenComboCard[0]:
                        continue

                    if card[3] == chosenComboCard[3]:
                        chosenCardToDelete = card
                        break
                    elif card[3] > chosenComboCard[3]:
                        chosenCardToDelete = card
                    elif card[3] < chosenComboCard[3]:
                        if chosenCardToDelete != None:
                            if chosenCardToDelete[3] < card[3]:
                                chosenCardToDelete = card
                        else:
                            chosenCardToDelete = card

                deck.remove(chosenCardToDelete)

        return deck


    #TODO: Once the loading function is set up incorporate loading the decks into the list of decks
    def generateDeck(self, color, n_iterations):
        i = 0
        listOfDecks = []
        while i < n_iterations:

            #generate the deck
            pileOfCards = self.gatherCards(color)

            cardIds = self.extractCardId(pileOfCards)

            pileOfCombos = self.gatherComboList(cardIds)

            pileOfCards = self.comboCheck(pileOfCards, pileOfCombos, cardIds)

            i = i+1
            listOfDecks.append(pileOfCards)
        return listOfDecks


if __name__ == "__main__":
    deckGen = DeckGenerator()
    listOfDecks = []
    color = "Green"
    color = color + " "
    i=0
    while i < 1:
        deck = deckGen.generateDeck(color)
        listOfDecks.append(deck)
        i=i+1
    fitness = fitnessFunction()
    fitness.fitness(listOfDecks[0])


