
# # # # # # # # # # # # # # College Family Generator # # # # # # # # # # # # #

# Section: Importing Modules

# Import Pandas library, used to store information about each child and parent
import pandas as pd

# Section End


# Section: Constants

SUBJECTMULTIPLIER = 1
CONTACTMULTIPLIER = 1
MEETINGMULTIPLIER = 1
ARTSMULTIPLIER = 1
SPORTSMULTIPLIER = 1
ENTERTAINMENTMULTIPLIER = 1
NIGHTOUTMULTIPLIER = 1

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

# Region: Panda Structures

# Parents : ID, email, name1, name2, name3, yearGoingInto, childrenAlready,
#           subjects, contactAmount, meetingPlaces, arts, sports, entertainment
#           , nightOut

# Children: ID, email, name, subject, contactAmount, meetingPlaces, arts,
#           sports, entertainment, nightOut

# Region End

# Section End


# Section: Evaluation Functions

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

    matchScore += SUBJECTMULTIPLIER * evaluateSubject(match)
    matchScore += CONTACTMULTIPLIER * evaluateContact(match)
    matchScore += MEETINGMULTIPLIER * evaluateMeeting(match)
    matchScore += ARTSMULTIPLIER * evaluateArts(match)
    matchScore += SPORTSMULTIPLIER * evaluateSports(match)
    matchScore += ENTERTAINMENTMULTIPLIER * evaluateEntertainment(match)
    matchScore += NIGHTOUTMULTIPLIER * evaluateNightOut(match)

    return matchScore


def evaluateSubject(parentID, childID):
    print("Evaluating")

    score = 0

    return score


def evaluateContact(parentID, childID):

    score = 0

    parentContact = parents.loc[parentID]["contactAmount"]
    childrenContact = children.loc[childID]["contactAmount"]

    score += compareScale(parentContact, childrenContact)

    return score


def evaluateMeeting(parentID, childID):

    parentActivities = parents.loc[parentID]["meetingPlaces"]
    childrenActivities = children.loc[childID]["meetingPlaces"]

    score = compareActivities(parentActivities, childrenActivities)

    return score


def evaluateArts(parentID, childID):

    parentActivities = parents.loc[parentID]["arts"]
    childrenActivities = children.loc[childID]["arts"]

    score = compareActivities(parentActivities, childrenActivities)

    return score


def evaluateSports(parentID, childID):

    parentActivities = parents.loc[parentID]["sports"]
    childrenActivities = children.loc[childID]["sports"]

    score = compareActivities(parentActivities, childrenActivities)

    return score


def evaluateEntertainment(parentID, childID):
    print("Evaluating")

    score = 0

    return score


def evaluateNightOut(parentID, childID):
    print("Evaluating")

    score = 0

    return score


def formatCell(array):

    # Remove spaces from excel formatCell
    # Reason: spaces throw off intersection comparison
    noSpaceArray = array.replace(" ", "")

    # Split by ',' into all activities chosen
    splitArray = noSpaceArray.split(",")

    # Save as a set -> we need set operations later on
    finalArray = set(splitArray)

    return finalArray


def compareActivities(parentActivities, childActivities):

    parentActivities = formatCell(parentActivities)
    childActivities = formatCell(childActivities)

    sharedActivities = parentActivities.intersection(childActivities)
    # totalActivities = parentActivities.union(childActivities)
    # percentageSharedTotal = 100 * len(sharedActivities)/len(totalActivities)
    percentageSharedChild = (100 * len(sharedActivities)/len(
        childActivities))

    print(sharedActivities)
    print(childActivities)

    # Convert percentage to score out of 10, to 1 decimal place
    score = round(percentageSharedChild / 10, 1)

    #    print("Parent {0}  with Child {1}".format(parentID, childID))#
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


def compareScale(value1, value2):

    difference = abs(value1 - value2)

    if difference == 0:
        return 10
    elif difference == 1:
        return 5
    elif difference == 2:
        return 2
    else:
        return 0


# Section End


# Section: Forming Allocation Data Structure

# row = parents.loc[0]
# email = row["email"]

# Allocation stored in 2D Array
allocation = []

# Add Parents to allocation
# For each parent in the panda
for index, row in parents.iterrows():
    # Each Parent has 3 child 'slots', so add 3 arrays
    for i in range(3):
        allocation.append([row["ID"], -1])

# for row in allocation:
#    print(row)

# Region: Allocation Structure

# Allocation = [ [ParentID, ChildID], [ParentID, ChildID], ... ]

# Where ParentID repeats 3 times (3 child slots)
# [
#   [0, -1], [0, -1], [0, -1],
#   [1, -1], [1, -1], [1, -1],
#   [2, -1], [2, -1], [2, -1],
#     ...  ,   ...  ,   ...  ,
# ]

# Region End

# Section End

for i in range(5):
    print(evaluateSports(0, i))
