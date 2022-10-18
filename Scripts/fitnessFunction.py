from collections import Counter

import Scripts.deckGenerator
import math


class fitnessFunction():
    def __init__(self):
        self.file = ""

    def fitness(self, deck):
        #determine fitness of the decks
        #measure the distance between our optimal mana curve and the decks mana curve
        #determine the points for optimal curve
        #take in points for the decks mana curve
        #compare the difference and give a score based on this
        #lose points if the deck has more than 4 of the same card
        #IN FUTURE: have multiple mana curves for different turn formats e.g turn 3 format and a turn 4 format have slightly different mana curves
        #Optimal curve format: 1cmc, 2cmc, 3cmc, 4cmc, etc

        #MANA CURVE ==========================
        optimalManaCurveDict = {1: 9, 2: 13, 3: 9, 4: 3} #current mana curve: turn 4 format
        decksManaCurveDict = self.getManaCurve(deck) #get decks mana curve
        manaCurveScore = 0
        for cost, quantity in decksManaCurveDict.items():
            score = quantity
            if cost in optimalManaCurveDict:
                score = optimalManaCurveDict[cost]-quantity

            manaCurveScore = manaCurveScore - abs(score)

        # Quantity ==========================
        #if the quantity of a card is above 4 points are lost for each card - ideally this should be 0
        quantityDict = self.getQuantity(deck)
        quantityScore = 0
        for card, quantity in quantityDict.items():
            score = 0
            if quantity > 4:
                score = 100
            quantityScore = quantityScore - abs(score)

        comboScore = self.getComboScore(deck)


        #TODO: card type scoring e.g number of creatures to instant/sorcery cards

        # FITNESS SCORE ==========================
        fitnessScore = 0
        fitnessScore = fitnessScore - abs(manaCurveScore) - abs(quantityScore) - abs(comboScore) #unsure what x should be but closer to 0 means a more optimal solution
        return fitnessScore

    def getManaCurve(self, deck):
        manaCurve = {}
        manaCostList = []
        for card in deck:
            manaCost = card[3]
            manaCostList.append(manaCost)

        manaCurve = Counter(manaCostList)
        return manaCurve

    def getQuantity(self, deck):
        quantityOfCards = {}
        listOfCards = []
        for card in deck:
            c = card[0]
            listOfCards.append(c)
        quantityOfCards = Counter(listOfCards)
        return quantityOfCards

    def getComboScore(self, deck):
        score = 0
        prob = 0
        comboList = []
        cardIds = []
        deckCombos = []

        deckGen = Scripts.deckGenerator.DeckGenerator()
        cardIds = deckGen.extractCardId(deck)
        comboList = deckGen.gatherComboList(cardIds) #Gathers combos that have at least 1 card from the deck in them
        if len(comboList) == 0:
            score = 100
            return score
        cardsQuantity = self.getQuantity(deck)

        #Wrap this in a loop to loop over every combo in the deck
        deckCombos = deckGen.getComboListFromDeck(cardIds, comboList) #Gets all combos that exist in the deck
        if len(deckCombos) == 0:
            score = 100
            return score
        if len(deckCombos) > 1:
            for combo in deckCombos:
                p_c1 = combo[0]
                p_c2 = combo[1]
                p_c1_qty = cardsQuantity.get(p_c1)
                p_c2_qty = cardsQuantity.get(p_c2)
                prob = self.getProbability(p_c1_qty, p_c2_qty)
                score = self.getProbabilityScore(prob) + score
        else:
            combo = deckCombos[0]
            p_c1 = combo[0]
            p_c2 = combo[1]
            p_c1_qty = cardsQuantity.get(p_c1)
            p_c2_qty = cardsQuantity.get(p_c2)
            prob = self.getProbability(p_c1_qty, p_c2_qty)
            score = self.getProbabilityScore(prob)

        return score

    def getProbability(self, p_c1_qty, p_c2_qty):
        #Work out the conditional probability of drawing the combo from a 60 card deck
        #The chance of drawing card in opening hand
        #if one is in opening hand chance of drawing card next turn
        if p_c1_qty != p_c2_qty:
            probabilityOfComboCard1 = self.hyperDist(1, 60, p_c1_qty, 7)  # Likelihood of drawing card1 within first hand draw
            probabilityOfComboCard2 = self.hyperDist(1, 59, p_c2_qty, 6)  # Likelihood of drawing card 2 within first hand draw after card 1 has been drawn
            combination1 = probabilityOfComboCard1 * probabilityOfComboCard2
            conditionalProbOfCombo1 = combination1 / probabilityOfComboCard1
            probabilityOfComboCard2 = self.hyperDist(1, 60, p_c2_qty, 7)
            probabilityOfComboCard1 = self.hyperDist(1, 59, p_c1_qty, 6)
            combination2 = probabilityOfComboCard2 * probabilityOfComboCard1
            conditionalProbOfCombo2 = combination2 / probabilityOfComboCard2
            prob = conditionalProbOfCombo1 * conditionalProbOfCombo2
        else:
            probabilityOfComboCard1 = self.hyperDist(1, 60, p_c1_qty, 7)
            probabilityOfComboCard2 = self.hyperDist(1, 59, p_c2_qty, 6)
            prob = probabilityOfComboCard1 * probabilityOfComboCard2

        prob = round(prob, 2)
        return prob

    def getProbabilityScore(self, prob):
        score = 1/prob
        return score

    def combiNoRep(self, n, r): #Combinations without repitition
        x = math.factorial(n)/(math.factorial(r)*(math.factorial(n-r)))
        return x

    def hyperDist(self, drawnCombo, total, totalCombo, drawn):
        x = ((self.combiNoRep(totalCombo, drawnCombo)*self.combiNoRep(total-totalCombo, drawn-drawnCombo)) /
             self.combiNoRep(total, drawn))
        return x

    def run(self, p_c1_qty, p_c2_qty):
        print("Running fitness function")
        if p_c1_qty != p_c2_qty:
            probabilityOfComboCard1 = self.hyperDist(1, 60, p_c1_qty, 7) #Likelihood of drawing card1 within first hand draw
            probabilityOfComboCard2 = self.hyperDist(1, 59, p_c2_qty, 6) #Likelihood of drawing card 2 within first hand draw after card 1 has been drawn
            combination1 = probabilityOfComboCard1 * probabilityOfComboCard2
            conditionalProbOfCombo1 = combination1 / probabilityOfComboCard1
            probabilityOfComboCard2 = self.hyperDist(1, 60, p_c2_qty, 7)
            probabilityOfComboCard1 = self.hyperDist(1, 59, p_c1_qty, 6)
            combination2 = probabilityOfComboCard2 * probabilityOfComboCard1
            conditionalProbOfCombo2 = combination2 / probabilityOfComboCard2
            print("card1: ", conditionalProbOfCombo1)
            print("card2: ", combination2)
            prob = conditionalProbOfCombo1 * conditionalProbOfCombo2
            return prob
        else:
            probabilityOfComboCard1 = self.hyperDist(1, 60, p_c1_qty, 7)
            probabilityOfComboCard2 = self.hyperDist(1, 59, p_c2_qty, 6)
            prob = probabilityOfComboCard1 * probabilityOfComboCard2
            return prob


if __name__ == "__main__":
    fitness = fitnessFunction()
    x = fitness.run(2, 2)
    print(x)