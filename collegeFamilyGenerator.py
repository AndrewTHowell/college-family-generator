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

# Used to generate random allocations
from random import shuffle

# Section End

# Section: Constants

# Max Number of Children per Parent
SLOTS = 3

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

# Section End

# Section: CSV files

# Location of Folder containing CSV Files
CSVLocation = ("D:\\howel\\OneDrive - Durham University\\Exec\\VP Development"
               "\\College Families\\college-family-generator\\Import Files")

global parents
global children

# Create the Parents Panda, extracting info from CSV files
parents = pd.read_csv("{0}\\Parents.csv".format(CSVLocation), skiprows=1,
                      names=["email", "name1", "name2", "name3",
                             "yearGoingInto", "childrenAlready", "subjects",
                             "contactAmount", "meetingPlaces",
                             "arts", "sports", "entertainment", "nightOut"],
                      usecols=range(1, 14))

# Create the Parents Panda, extracting info from CSV files
children = pd.read_csv("{0}\\Children.csv".format(CSVLocation), skiprows=1,
                       names=["email", "name", "subjects",
                              "contactAmount", "meetingPlaces",
                              "arts", "sports", "entertainment", "nightOut"],
                       usecols=range(1, 10))

# Add ID columns to both Pandas
parents.insert(0, "ID", range(0, len(parents)))
children.insert(0, "ID", range(0, len(children)))

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

# Section: Forming Allocation Data Structure

# row = parents.loc[0]
# email = row["email"]

# Allocation stored in 2D Array
allocation = []

# Add Parents to allocation
# For each parent in the panda
for index, row in parents.iterrows():
    # Each Parent has SLOTS child 'slots', so add SLOTS arrays
    for i in range(SLOTS):
        allocation.append([row["ID"], -1])


# Region: Allocation Structure

# Allocation = [ [ParentID, ChildID], [ParentID, ChildID], ... ]

# Where ParentID repeats SLOTS times (SLOTS child slots)
# [
#   [0, -1], [0, -1], [0, -1],
#   [1, -1], [1, -1], [1, -1],
#   [2, -1], [2, -1], [2, -1],
#     ...  ,   ...  ,   ...  ,
# ]

# Region End


# Section End

# Section: Evaluation Functions

# Region: Evaluation Function Stack

# Returns a score for this allocation
def evaluateAllocation(allocation):

    allocationScore = 0

    # Collect scores for each match
    for match in allocation:
        allocationScore += evaluateMatching(match)

        # Evaluate parents -> year going into, already have children

        # Evaluate Year Going Into
        yearGoingInto = parents.loc[match[0]//SLOTS]["yearGoingInto"]
        if yearGoingInto == "Year 2":
            allocationScore += MULTIPLIERS["yearGoingInto"] * 10
        elif yearGoingInto == "Year 3":
            allocationScore += MULTIPLIERS["yearGoingInto"] * 0
        elif yearGoingInto == "Year 4":
            allocationScore += MULTIPLIERS["yearGoingInto"] * -10

        # Evaluate Children Already
        childrenAlready = parents.loc[match[0]//SLOTS]["childrenAlready"]
        if childrenAlready == "Yes":
            allocationScore += MULTIPLIERS["childrenAlready"] * -10
        elif childrenAlready == "No":
            allocationScore += MULTIPLIERS["childrenAlready"] * 10

    return allocationScore


# Returns a score for this matching
def evaluateMatching(match):

    matchScore = 0

    # If match has not been encountered before
    parentID, childID = match

    # If childID is negative, slot is empty so no need to evaluate
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

    return matchScore


'''def evaluateSubject(parentID, childID):

    print("Evaluating Subject")

    attrID = "subjects"

    # Gets activities info of Parent
    pSubjects = parents.loc[parentID//SLOTS][attrID]
    cSubjects = children.loc[childID][attrID]

    # Format cells -> remove spaces, split into list of subjects, become set
    pSubjects = formatCell(pSubjects)
    cSubjects = formatCell(cSubjects)

    # If subjects have not been encountered before
    if evaluateMatching.values[attrID][pSubjects][cSubjects] == -1:

        score = 0

        # Subject evaluation system ###########################################

        evaluateMatching.values[attrID][pSubjects][cSubjects] = score

    # If subjects have been encountered before
    else:
        score = evaluateMatching.values[attrID][pSubjects][cSubjects]

    return score'''


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

    '''# If activities have not been encountered before
    if evaluateMatching.values[attrID][pActivities][cActivities] == -1:
        score = compareActivities(pActivities, cActivities)

        evaluateMatching.values[attrID][pActivities][cActivities] = score

    # If activities have been encountered before
    else:
        score = evaluateMatching.values[attrID][pActivities][cActivities]'''

    return score


# Division: Initialising Static Function Variables

# Need to have dynamic array size for each attribute ##########################

evaluateMatching.values = {}

# Initialising (parent x child) array to hold previous match scores
evaluateMatching.values["matches"] = []
for parent in range(NUMBEROFPARENTSLOTS):
    parentSlot = []
    for child in range(NUMBEROFCHILDREN):
        parentSlot.append(-1)
    evaluateMatching.values["matches"].append(parentSlot)

# print(evaluateMatching.values["matches"])

'''# For each Activity attribute, initialise a dictionary
# Structure: {attr: {parentActivities: childActivities}}
for attr in POSSIBLEVALUES.keys():
    # If value is a list (of activities), Initialise a dict
    if isinstance(POSSIBLEVALUES[attr], list):
        evaluateMatching.values[attr] = {}
        # print("Initialising for {0}".format(attr))'''

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

    i = 0
    while i < len(allocation):
        # Extract parentID and childIDs
        childIDs = []
        for j in range(SLOTS):
            [parentIDSlot, childID] = allocation[i+j]
            childIDs.append(childID)
        parentID = parentIDSlot // 3

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

        i += SLOTS


# Section End

# Section: Simulated Annealing

# Region: Constants

MAXTEMP = 15
ALPHA = 0.85


# Region End

def schedule(t):
    T = MAXTEMP * power(ALPHA, t)

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

    print(allIDList)

    randomAllocation = shuffle(allIDList)

    return randomAllocation


# Section End

# Section: Main Functions

# Evaluate every permutation of allocations, finding the highest scoring
def main():
    optimumAllocation = []
    optimumAllocationScore = 0

    startTime = time.time()

    # # Add Simulated Annealing here # # # # #
    generateStartAllocation()

    timeElapsed = time.time() - startTime

    print("Optimum Allocation: {0}".format(optimumAllocation))
    print("Optimum Allocation Score: {0:.1f}".format(optimumAllocationScore))
    print("{0:02}:{1:02}".format(round(timeElapsed // 60), (
                                 round(timeElapsed % 60))))


# Section End

print("Make sure Sam Attfield Parents for Jack Peachey")
print("I.E. remove Jack from Children.csv"
      " and add him to Samuel Attfield's Family")
print("If emailing out, remember to email Sam that he also has Jack")

generateStartAllocation()

# emailAllocation([[0, 0], [1, 2], [2, 3], [3, -3], [4, -2], [5, -1]])

# main()

# Send email to self, notifiying me that the code has finished
# emailer = Emailer()
# emailer.send("howelldrew99@gmail.com",
#              "Code Finished",
#              "College Family Generator has finished")

"""
perms = permutations(chain(childIDRange, nullIDRange))
# perms = [(0, 2, 1, -1, -2, -3)]

i = 0
for perm in perms:
    allocation = []
    for slotID in range(NUMBEROFPARENTSLOTS):
        # print(slotID, perm[slotID])
        allocation.append([slotID, perm[slotID]])
    allocationScore = evaluateAllocation(allocation)

    # print(perm)
    # print(allocationScore)

    if allocationScore > optimumAllocationScore:
        optimumAllocation = allocation
        optimumAllocationScore = allocationScore

    if i == 500:
        break
    i += 1
"""

# Integrate Simulated Annealing and Test

# Export allocations as JSON

# Evaluate child interest similarities
