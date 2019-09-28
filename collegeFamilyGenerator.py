# Section: Importing Modules

# Used to store information about each child and parent
import pandas as pd

# Used to find all permutations of allocations
# from itertools import permutations, chain

# Used to time the running code
import time

# Used to send Facebook message to me once the code has finished
# from twilio.rest import Client

# Used to email me when the generator is finished
from Emailer import Emailer

# Used to reformat Attributes from camelCase to Camel case
from re import findall

# Used to raise x to the power of y (power(x,y) = x^y)
from math import pow as power

# Used to find exponential of x (exp(x) = e^x)
from math import exp

# Used to generate random allocations
from random import shuffle

# Used to do something with probability x
from random import random

# Used to choose two parent slots to swap
from random import sample

# Section End

# Section: Constants

# Max Number of Children per Parent
SLOTS = 3

# Location of Folder containing CSV Files
CSVLOCATION = ("C:\\Users\\howel\\OneDrive - Durham University\\Exec\\"
               "VP Development\\College Families\\college-family-generator\\"
               "Import Files\\")

MULTIPLIERS = {"yearGoingInto":   1,
               "childrenAlready": 1,
               "subjects":        1,
               "contactAmount":   1,
               "meetingPlaces":   1,
               "arts":            1,
               "sports":          1,
               "entertainment":   1,
               "nightOut":        1}

POSSIBLEVALUES = {"yearGoingInto":   ["Year 2",
                                      "Year 3",
                                      "Year 4"],

                  "childrenAlready": ["Yes",
                                      "No"],

                  "subjects":        [],
                  "contactAmount":   range(1, 6),

                  "meetingPlaces":   ["Clubbing / Bars",
                                      "Pub",
                                      "Sit Down Meal",
                                      "Cafe",
                                      "Cinema",
                                      "Theatre",
                                      "Takeaway in front of a TV",
                                      "Prefer not to meet up"],

                  "arts":            ["Acting",
                                      "Bands",
                                      "Dancing",
                                      "Singing"],

                  "sports":          ["Athletics",
                                      "Badminton",
                                      "Basketball",
                                      "Cheerleading",
                                      "Cricket",
                                      "Cycling",
                                      "Dance",
                                      "Darts",
                                      "Football",
                                      "Gymnastics",
                                      "Hockey",
                                      "Horse Riding",
                                      "Lacrosse",
                                      "Martial Arts",
                                      "Netball",
                                      "Pool",
                                      "Rounders",
                                      "Rowing",
                                      "Rugby",
                                      "Squash",
                                      "Swimming",
                                      "Table Tennis",
                                      "Tennis",
                                      "Ultimate Frisbee",
                                      "Volleyball"],

                  "entertainment":   ["Films",
                                      "Gaming",
                                      "Music",
                                      "TV Shows"],

                  "nightOut":        range(1, 6)}

NUMITERATIONS = 10000

# Section Ends

# Section: CSV files

global parents
global children

# Create the Parents Panda, extracting info from CSV files
parents = pd.read_csv("{0}Parents.csv".format(CSVLOCATION), skiprows=1,
                      names=["email", "name1", "name2", "name3",
                             "yearGoingInto", "childrenAlready", "subjects",
                             "contactAmount", "meetingPlaces",
                             "arts", "sports", "entertainment", "nightOut"],
                      usecols=range(1, 14))

# Create the Parents Panda, extracting info from CSV files
children = pd.read_csv("{0}Children.csv".format(CSVLOCATION), skiprows=1,
                       names=["email", "name", "subjects",
                              "contactAmount", "meetingPlaces",
                              "arts", "sports", "entertainment", "nightOut"],
                       usecols=range(1, 10))

# Add ID columns to both Pandas
parents.insert(0, "ID", range(len(parents)))
children.insert(0, "ID", range(len(children)))

# Fill in missing values (empty cells) as empty strings
parents = parents.fillna("")
children = children.fillna("")

# Log Constants
NUMBEROFCHILDREN = len(children.index)
NUMBEROFPARENTS = len(parents.index)
NUMBEROFPARENTSLOTS = SLOTS * NUMBEROFPARENTS


# Region: Panda Structures

# Parents : ID, email, name1, name2, name3, yearGoingInto, childrenAlready,
#           subjects, contactAmount, meetingPlaces, arts, sports, entertainment
#           , nightOut

# Children: ID, email, name, subject, contactAmount, meetingPlaces, arts,
#           sports, entertainment, nightOut

# Region End

# Section End

# Section: Evaluation Functions

# Region: Evaluation Functions

# Returns a score for this allocation
def evaluateAllocation(allocation):

    allocationScores = []

    # Collect scores for each match
    for parentID in range(len(allocation)):

        matchScore = evaluateMatching([parentID, allocation[parentID]])

        allocationScores.append(matchScore)

    return allocationScores


# Returns a score for this matching
def evaluateMatching(match):

    matchScore = 0

    # If match has not been encountered before
    parentID, childID = match

    # If childID is positive, slot is not empty so need to evaluate
    if childID >= 0:

        if evaluateMatching.values["matches"][parentID][childID] == -1:
            # matchScore += (MULTIPLIERS["subject"]
            #                * evaluateSubject(parentID, childID))

            for attr in ["subjects",
                         "meetingPlaces",
                         "arts",
                         "sports",
                         "entertainment"]:
                matchScore += (MULTIPLIERS[attr]
                               * evaluateActivities(parentID, childID, attr))

            for attr in ["contactAmount", "nightOut"]:
                matchScore += (MULTIPLIERS[attr]
                               * evaluateByScale(parentID, childID, attr))

            evaluateMatching.values["matches"][parentID][childID] = matchScore

        # If match has been encountered before
        else:
            matchScore = evaluateMatching.values["matches"][parentID][childID]

        if childID >= 0:
            # Evaluate Parent suitability
            # Evaluate Year Going Into
            yearGoingInto = parents.loc[parentID//SLOTS]["yearGoingInto"]
            if yearGoingInto == "Year 2":
                matchScore += MULTIPLIERS["yearGoingInto"] * 10
            elif yearGoingInto == "Year 3":
                matchScore += MULTIPLIERS["yearGoingInto"] * 5
            elif yearGoingInto == "Year 4":
                matchScore += MULTIPLIERS["yearGoingInto"] * 0

            # Evaluate Children Already
            childrenAlready = parents.loc[parentID//SLOTS]["childrenAlready"]
            if childrenAlready == "Yes":
                matchScore += MULTIPLIERS["childrenAlready"] * 0
            elif childrenAlready == "No":
                matchScore += MULTIPLIERS["childrenAlready"] * 10

    return matchScore


def evaluateByScale(parentID, childID, attr):

    # Gets values
    parentValue = parents.loc[parentID//SLOTS][attr]
    childrenValue = children.loc[childID][attr]

    score = compareScale(parentValue, childrenValue)

    return score


def evaluateActivities(parentID, childID, attrID):

    # print("Evaluating Activity")

    # Gets activities info of Parent
    pActivities = parents.loc[parentID//SLOTS][attrID]
    cActivities = children.loc[childID][attrID]

    # Format cells -> remove spaces, split into list of activities, become set
    pActivities = formatCell(pActivities)
    cActivities = formatCell(cActivities)

    score = compareActivities(pActivities, cActivities)

    return score


# Division: Initialising Static Function Variables

evaluateMatching.values = {}

# Initialising (parent x child) array to hold previous match scores
evaluateMatching.values["matches"] = []
for parent in range(NUMBEROFPARENTSLOTS):
    parentSlot = []
    for child in range(NUMBEROFCHILDREN):
        parentSlot.append(-1)
    evaluateMatching.values["matches"].append(parentSlot)

# print(evaluateMatching.values["matches"])


# Division End

# Region End

# Region: Comparator and Format Functions

# Formats cells containing Activities ready for compareActivities()
def formatCell(array):

    # Remove spaces from excel formatCell
    # Reason: spaces throw off intersection comparison
    noSpaceArray = array.replace(" ", "")

    # Split by ',' into all activities chosen
    splitArray = noSpaceArray.split(",")

    # Save as a set -> we need set operations later on
    finalArray = set(splitArray)

    return finalArray


# Compares parent and child lists of activities
# Scores them based on the percentage of Child activities shared by the Parents
def compareActivities(parentActivities, childActivities):

    # Percentage of child's activities shared by parents calculated
    sharedActivities = parentActivities.intersection(childActivities)
    # totalActivities = parentActivities.union(childActivities)
    # percentageSharedTotal = 100 * len(sharedActivities)/len(totalActivities)
    percentageSharedChild = (100 * len(sharedActivities)/len(
                                                            childActivities))

    # print(sharedActivities)
    # print(childActivities)

    # Convert percentage to score out of 10, to 1 decimal place
    score = round(percentageSharedChild / 10, 1)

    #    print("Parent {0}  with Child {1}".format(parentID, childID))
    #    print()
    #    print("Parent {0}: ".format(parentID), end='')
    #    print(parentMeetingPlaces)
    #    print("Child {0}: ".format(childID), end='')
    #    print(childrenMeetingPlaces)
    #    print()
    #    print("Shared Activities: ", end='')
    #    print(sharedActivities)
    #    # print("Total Activities: ", end='')
    #    # print(totalActivities)
    #    print("Percentage Shared (Total): ", end='')
    #    print(str(percentageSharedTotal) + "%")
    #    print("Percentage Shared (Child): ", end='')
    #    print(str(percentageSharedChild) + "%")
    #    print()
    #    print()

    return score


# Compares parent and child scalar scores
# Scores them based on their difference along the scale
# e.g. compareScale(5,2) < compareScale(3,1) < compareScale(2,2)
def compareScale(value1, value2):

    # Find absolute (positive) difference between two scale values
    # print(value1, type(value1))
    # print(value2, type(value2))
    difference = abs(value1 - value2)

    # print(value1, value2)
    # print(difference)

    # Scoring system based off of difference, further away -> smaller score
    if difference == 0:
        return 10
    elif difference == 1:
        return 5
    elif difference == 2:
        return 2
    else:
        return 0


# Region End

# Section End

# Section: Emailer Functions

def formatForShared(string):
    if string == "":
        return set()

    # Split by ',' into all activities chosen
    array = string.split(",")

    for i in range(len(array)):
        if array[i][0] == " ":
            array[i] = array[i][1:]

    # Save as a set -> we need set operations later on
    finalSet = set(array)

    return finalSet


def emailAllocation(allocation):

    emailer = Emailer()

    for parentID in range(len(allocation) // 3):
        # Extract childIDs
        childIDs = []
        for slotNum in range(SLOTS):
            childID = allocation[parentID + slotNum]
            childIDs.append(childID)

        parentNames = [parents.loc[parentID]["name1"],
                       parents.loc[parentID]["name2"],
                       parents.loc[parentID]["name3"]]

        parentNames = list(filter(None, parentNames))

        if len(parentNames) == 1:
            message = "Hi {0},\n\n".format(parentNames[0])
        if len(parentNames) == 2:
            message = "Hi {0} and {1},\n\n".format(parentNames[0],
                                                   parentNames[1])
        if len(parentNames) == 3:
            message = "Hi {0}, {1} and {2},\n\n".format(parentNames[0],
                                                        parentNames[1],
                                                        parentNames[2])

        childIDs = [child for child in childIDs if child >= 0]

        if len(childIDs) == 0:
            message += ("Unfortunately, you weren't assigned any children this"
                        " year.\n")
            message += ("Matchings were based on who was most compatible, and"
                        " so some parents received multiple children and some"
                        " received none"
                        "\n\n")
            message += ("However, thank you so much for volunteering to be a "
                        "College Parent.\n")

        else:
            message += ("Thank you so much for volunteering to be a College"
                        " Parent, here's some information on your new"
                        " children.\n")

            parentAttributes = {}
            # For each attribute, get parent attributes
            for attribute in ["subjects",
                              "meetingPlaces",
                              "arts",
                              "sports",
                              "entertainment"]:

                string = parents.loc[parentID][attribute]

                parentAttributes[attribute] = formatForShared(string)

            childNum = 1
            for childID in childIDs:
                message += "\nChild {0}".format(childNum)
                childNum += 1
                message += "\nName: {0}\nEmail Address: {1}\n".format(
                                                children.loc[childID]["name"],
                                                children.loc[childID]["email"])

                # Get shared interests
                for attribute in ["subjects",
                                  "meetingPlaces",
                                  "arts",
                                  "sports",
                                  "entertainment"]:

                    string = children.loc[childID][attribute]

                    childSet = formatForShared(string)

                    # Find common interests in Attribute
                    common = childSet.intersection(parentAttributes[attribute])

                    if len(common) != 0:
                        # Format Attribute for Email
                        attr = " ".join(findall('[A-Z][^A-Z]*',
                                                attribute[0].upper()
                                                + attribute[1:]))

                        message += ("Your common {0} are: {1}\n"
                                    .format(attr.lower(),
                                            ", ".join(list(common))))

            message += ("\nPlease contact your children as soon as possible"
                        " and introduce yourselves.\n\n")

            message += ("There will be a Parent's 'Informal' event held on"
                        " Friday, 11th October. Please make sure you encourage"
                        " your Freshers to go, it should be a really fun"
                        " evening and will allow you to get to know each other"
                        " better.\n")

        message += ("\n*** This is an automated email, sent out by your"
                    " VP Development. If you have any questions or issues,"
                    " please speak to him directly at vp@mildert.co.uk ***\n")

        message += ("\nKind Regards,\nAndrew's Computer :)")

        print("Message:")
        print(message)

        # emailer.send(parents.loc[parentID]["email"],
        # emailer.send("howelldrew99@gmail.com",
        #              "College Family Allocation",
        #              message)


# Section End

# Section: Simulated Annealing

def schedule(maxTemp, alpha, t):
    T = maxTemp * power(alpha, t)
    return T


def generateStartAllocation():

    # Get range of all children IDs
    childIDRange = range(NUMBEROFCHILDREN)
    # Convert to list of child IDs
    childIDList = list(childIDRange)

    # Parents slots not occupied by Children will be 'null' slots
    numberOfEmptySlots = NUMBEROFPARENTSLOTS - NUMBEROFCHILDREN
    nullIDRange = range(-1, -(numberOfEmptySlots + 1), -1)
    # Convert to list of null IDs
    nullIDList = list(nullIDRange)

    # Combine list of child and null IDs
    allIDList = childIDList + nullIDList

    # Randomly shuffles the ID list
    shuffle(allIDList)

    return allIDList


def simAnneal(maxTemp, alpha):

    currentState = generateStartAllocation()
    currentScores = evaluateAllocation(currentState)
    currentValue = sum(currentScores)

    bestState = currentState
    bestValue = currentValue

    temperature = maxTemp
    t = 0
    while temperature > 0.01:

        temperature = schedule(maxTemp, alpha, t)

        # Set temporary next state
        nextState = currentState
        nextScores = currentScores
        nextValue = currentValue

        # Make random swap in allocation (don't swap empty slots)
        swapIDs = sample(list(range(len(currentState))), 2)
        while nextState[swapIDs[0]] < 0 and nextState[swapIDs[1]] < 0:
            swapIDs = sample(list(range(len(currentState))), 2)

        temp = nextState[swapIDs[0]]
        nextState[swapIDs[0]] = nextState[swapIDs[1]]
        nextState[swapIDs[1]] = temp

        # Reevaluate swapped allocation
        newValues = 0
        oldValues = 0
        for swapID in swapIDs:
            newValue = evaluateMatching([swapID, currentState[swapID]])
            newValues += newValue
            oldValues += currentScores[swapID]
        nextValue += newValues - oldValues

        deltaE = nextValue - currentValue

        # print(nextScores, nextValue)

        # If nextState is better, move to it
        if deltaE >= 0:
            currentState = nextState
            currentValue = nextValue
            currentScores = nextScores

            # See if it is best allocation so far
            if nextValue > bestValue:
                bestValue = nextValue
                bestState = nextState

        # If not better, move with probability...
        else:
            probabilityToMove = exp(deltaE/temperature)

            if random() < probabilityToMove:
                currentState = nextState
                currentValue = nextValue
                currentScores = nextScores

                # input("Swapped to worse")

        t += 1

    return [bestState, bestValue]


# Section End

# Section: Main Functions

# Evaluate every permutation of allocations, finding the highest scoring
def main():

    startTime = time.time()

    maxTemp = 100
    alpha = 0.9
    bestAllocation, bestValue = simAnneal(maxTemp, alpha)

    timeElapsed = time.time() - startTime

    print("Optimum Allocation: {0}".format(bestAllocation))
    print("Optimum Allocation Score: {0:.1f}".format(bestValue))
    print("{0:02}:{1:02}".format(round(timeElapsed // 60), (
                                 round(timeElapsed % 60))))


# Section End

print("Make sure Sam Attfield Parents for Jack Peachey")
print("I.E. remove Jack from Children.csv"
      " and add him to Samuel Attfield's Family")
print("If emailing out, remember to email Sam that he also has Jack")

main()

# Send email to self, notifiying me that the code has finished
# emailer = Emailer()
# emailer.send("howelldrew99@gmail.com",
#              "Code Finished",
#              "College Family Generator has finished")
