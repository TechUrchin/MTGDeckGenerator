from random import randint, random
from deckGenerator import *
from fitnessFunction import *
import time
import sys

class geneticAlgorithm():
    def __init__(self):
        self.file = ""

    def parentCreation(self, n_iter, n_pop, r_mut, r_cross):
        deckGen = DeckGenerator()
        color = 'Green '
        numberOfDecks = n_pop
        # need a matrix containing a list of decks
        listOfDecks = deckGen.generateDeck(color, numberOfDecks)
        fitness = fitnessFunction()

        bestDeck = 0
        bestDeckScore = -100

        # needs to enumerate through a number of generations
        for gen in range(n_iter):

            # need to call the fitness function to evaluate all the decks
            scores = []
            for deck in listOfDecks:
                score = fitness.fitness(deck)
                scores.append(score)

            for i in range(numberOfDecks):
                if scores[i] > bestDeckScore:
                    bestDeck = listOfDecks[i]
                    bestDeckScore = scores[i]
                    print("New best deck: ", bestDeck)
                    print("Best Deck Score: ", bestDeckScore)

            # call the tournament selection for each position in the population to create a list of parents
            selectedDecks = []
            for i in range(numberOfDecks):
                selectedDeck = self.selection(listOfDecks, scores)
                selectedDecks.append(selectedDeck)

            # put all children in a list
            # loop over population
            # create children through crossover
            # check if mutation occurs
            # add children to next generation
            # population is overridden with new generation

            nextGenDecks = []
            for i in range(0, numberOfDecks, 2):
                parentDeck1, parentDeck2 = selectedDecks[i], selectedDecks[i+1]
                childrenDecks = self.crossover(parentDeck1, parentDeck2, r_cross)
                for childDeck in childrenDecks:
                    self.mutation(childDeck, r_mut, color)
                    nextGenDecks.append(childDeck)

            listOfDecks = nextGenDecks
        return [bestDeck, bestDeckScore]




    #Tournament selection - takes list of decks and returns 1 deck aka parent
    #return the highest fitness scoring parent
    def selection(self, listOfDecks, scores, k=5):
        numberOfDecks = len(listOfDecks)
        selectedDeck = randint(0, numberOfDecks-1)

        for i in range(k):
            randomDeck = randint(0, numberOfDecks-1)
            if scores[randomDeck] > scores[selectedDeck]:
                selectedDeck = randomDeck

        return listOfDecks[selectedDeck]



    def crossover(self, parentDeck1, parentDeck2, r_cross):
        #create the crossover function that takes 2 parents, copies them onto the children
        childDeck1, childDeck2 = parentDeck1.copy(), parentDeck2.copy()

        if random() < r_cross:
            crossOverPoint = randint(1, len(parentDeck1)-2)
            # Then selects a point to split on to perform the crossover
            childDeck1 = parentDeck1[:crossOverPoint] + parentDeck2[crossOverPoint:]
            childDeck2 = parentDeck2[:crossOverPoint] + parentDeck1[crossOverPoint:]
        return[childDeck1, childDeck2]

    def mutation(self, deck, r_mut, color):
        deckGen = DeckGenerator()
        for card in range(len(deck)):
            if random() < r_mut:
                deck[card] = deckGen.getRandomCard(color)

        #This will add flavour to the algorithm
        #run a for loop that iterates over the deck and if the random number is less than the mutation value then
        #get a random card from x colour e.g select a random green card or if two colours, choose a colour and then select a random card

    def run(self):
        # command = input("Do you want to load a deck? [y/n]")
        # if command == "y":
        #     #loaddeck
        # else:
        start = time.time()
        #number of iterations
        n_iterations = 5
        n_population = 1000
        r_mutationChance = 0.2
        r_crossoverRate = 0.9
        ultimateDeck = self.parentCreation(n_iterations, n_population, r_mutationChance, r_crossoverRate)
        if ultimateDeck[0] != 0:
            f = fitnessFunction()
            manaCurve = f.getManaCurve(ultimateDeck[0])
            quantityCards = f.getQuantity(ultimateDeck[0])
            print("Deck: ", ultimateDeck[0])
            print("Deck Score: ", ultimateDeck[1])
            print("Deck Mana Curve: ", manaCurve)
            print("Card quantity: ", quantityCards)
            self.saveDeck(ultimateDeck, n_population, n_iterations)
        else:
            print("No good decks were found!")
        total = time.time() - start
        print("time: ", total)
        self.saveTime(total, n_population, n_iterations)

    def saveDeck(self, deck, population, evolutions):
        deckOfCards = deck[0]
        fitnessScore = int(abs(deck[1]))
        file = open("pop"+str(population)+"evo"+str(evolutions)+".txt", "a")
        file.write("{} - {}\n".format(str(deckOfCards), str(fitnessScore)))

    def saveTime(self, time, population, evolutions):
        file = open("time.txt", "a")
        file.write("{}, {} - {}\n".format(str(population), str(evolutions), str(time)))



if __name__ == "__main__":
    genes = geneticAlgorithm()
    i = 0

    while i < 3:
        genes.run()
        i=i+1