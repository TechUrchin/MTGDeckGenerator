# SETTING UP THE DATABASE
Ensure you have MySQL installed.
Then import the dump file (I would recommend using MySQL workbench)
mysql -u root -p mtgdatabase < [filepath to project folder]/Database/Dump20210510.sql

Use this command within a MySQL to check it was successfully created:
use mtgdatabase
show tables

This should output two tables "cards" and "combos"

#To run the program
Run the genetic algorithm by:
python geneticAlgorithm.py

#To change the parameters
Open the geneticAlgorithm.py file and within the run method you will see the parameters
n_iterations - determines the number of evolutions
n_population - determines the number of decks
r_mutationChance - determines the chance of mutation
r_crossoverRate - determines the chance of crossover

Then within the parentCreation method you can edit the colour used to generate a deck.
Ensure you add a space after the colour name and the first letter of the colour must be capitalised:
"Green "
"Red "
"White "
"Black "
"Blue "