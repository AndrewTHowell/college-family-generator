### College Family Generator

import csv

def importCSVFile(filename):

    with open(filename) as file:
        # Setup reader
        csvReader = csv.reader(file)

        # Setup dictionary (to be returned)
        dictionary = {}
        
        personID = 0
        for row in csvReader:
            dictionary[personID] = row[1:] # Removes Timestamp Column
            personID += 1
            
        # Delete Header Row
        del dictionary[0]

        return dictionary


parents = importCSVFile("Test Data\Parents.csv")

print(parents[1])
