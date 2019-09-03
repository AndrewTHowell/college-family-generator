
# # # # # # # # # # # # # # College Family Generator # # # # # # # # # # # # #

# Section: Importing Modules

# Used to store information about each child and parent
import pandas as pd

# Used to find all permutations of allocations
from itertools import permutations, chain

# Used to time the running code
import time

# Used to send Facebook message to me once the code has finished
from twilio.rest import Client

# Section End


# Section: Constants

# Max Number of Children per Parent
SLOTS = 3

MULTIPLIERS = {"subjects":       1,
               "contactAmount":  1,
               "meetingPlaces":  1,
               "arts":           1,
               "sports":         1,
               "entertainment":  1,
               "nightOut":       1}

POSSIBLEVALUES = {"subjects":       [],
                  "contactAmount":  range(1, 6),

                  "meetingPlaces":  ["Clubbing / Bars",
                                     "Pub",
                                     "Sit Down Meal",
                                     "Cafe",
                                     "Cinema",
                                     "Theatre",
                                     "Takeaway in front of a TV",
                                     "Prefer not to meet up"],

                  "arts":           ["Acting",
                                     "Bands",
                                     "Dancing",
                                     "Singing"],

                  "sports":         ["Athletics",
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

                  "entertainment":  ["Films",
                                     "Gaming",
                                     "Music",
                                     "TV Shows"],

                  "nightOut":       range(1, 6)}

# Section End


# Section: Importing CSV files

# Location of Folder containing CSV Files
CSVLocation = ("D:\\howel\\OneDrive - Durham University\\Exec\\VP Development"
               "\\College Families\\college-family-generator\\Test Data")

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
                       names=["email", "name", "subject",
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

# Section End


# Section: Evaluation Functions

# Region: Evaluation Function Stack

# Returns a score for this allocation
def evaluateAllocation(allocation):

    allocationScore = 0

    # Collect scores for each match
    for parentChildMatching in allocation:
        allocationScore += evaluateMatching(parentChildMatching)

    # Evaluate parents -> year going into, already have children
    ###

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

            for attr in ["subject",
                         "meetingPlaces",
                         "arts",
                         "sports",
                         "entertainment"]:
                matchScore += (MULTIPLIERS[attr]
                               * evaluateActivites(parentID, childID, attr))

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

    print("Evaluating Activity")

    # Gets activities info of Parent
    pActivities = parents.loc[parentID//SLOTS][attrID]
    cActivities = children.loc[childID][attrID]

    # Format cells -> remove spaces, split into list of activities, become set
    pActivities = formatCell(pActivities)
    cActivities = formatCell(cActivities)

    # If activities have not been encountered before
    if evaluateMatching.values[attrID][pActivities][cActivities] == -1:
        score = compareActivities(pActivities, cActivities)

        evaluateMatching.values[attrID][pActivities][cActivities] = score

    # If activities have been encountered before
    else:
        score = evaluateMatching.values[attrID][pActivities][cActivities]

    return score


# Division: Initialising Static Function Variables

# Need to have dynamic array size for each attribute ##########################

evaluateMatching.values = {}

# Initialising (parent x child) array to hold previous match scores
evaluateMatching.values["matches"] = []
for parent in range(NUMBEROFPARENTSLOTS):
    parent = []
    for child in range(NUMBEROFCHILDREN):
        parent.append(-1)
evaluateMatching.values["matches"].append(parent)

# For each Activity attribute, initiliase a dictionary
# Structure: {attr: {parentActivities: childActivities}}
for attr in POSSIBLEVALUES.keys():
    # If value is a list (of activities), intiliase a dict
    if isinstance(POSSIBLEVALUES[attr], list):
        evaluateMatching.values[attr] = {}
        # print("Initialising for {0}".format(attr))

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


# Section: Main Functions


# Evaluate every permutation of allocations, finding the highest scoring
def main():
    optimumAllocation = []
    optimumAllocationScore = 0

    # Get range of all children IDs
    childIDRange = range(NUMBEROFCHILDREN)

    numberOfEmptySlots = NUMBEROFPARENTSLOTS - NUMBEROFCHILDREN
    nullIDRange = range(-1, -(numberOfEmptySlots + 1), -1)

    # print(NUMBEROFCHILDREN, numberOfEmptySlots)
    # print(NUMBEROFPARENTSLOTS)

    perms = permutations(chain(childIDRange, nullIDRange))
    # perms = [(0, 2, 1, -1, -2, -3)]

    startTime = time.time()

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

        # if i == 200:
        #     break
        # i += 1

    timeElapsed = time.time() - startTime

    print("Optimum Allocation: {0}".format(optimumAllocation))
    print("Optimum Allocation Score: {0:.1f}".format(optimumAllocationScore))
    print("{0:02}:{1:02}".format(round(timeElapsed // 60), (
                                 round(timeElapsed % 60))))

# Section End


main()

'''account_sid = 'AC739dd29454683bd010cf6d05f6a9aa9f'
auth_token = 'c03972aa1cd7455b509e54693f53c26b'
client = Client(account_sid, auth_token)

message = client.messages \\
                .create(
                     body="Code Finished",
                     from_='+441686207042',
                     to='+447792228849'
                 )
print(message.sid)'''

# ADD MEMOIZATION to all evaluation functions (bar evaluateAllocation)
# Add Parent-specific evaluation
# Integrate Simulated Annealing and Test
