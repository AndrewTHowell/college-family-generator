############### College Family Generator ###############

# Import Pandas library, used to store information about each child and parent
import pandas as pd

############### Importing CSV Files ###############

# Location of Folder containing CSV Files
CSVLocation = "D:\howel\OneDrive - Durham University\Exec\VP Development\College Families\college-family-generator\Test Data"

# Create the Parents Panda, extracting info from CSV files
parents = pd.read_csv("{0}\Parents.csv".format(CSVLocation), skiprows=1,
            names=["email","name1","name2","name3","yearGoingInto","childrenAlready",
                   "subjects","contactAmount","meetingPlaces",
                   "arts","sports","entertainment","nightOut"],
            usecols=range(1,14))

# Create the Parents Panda, extracting info from CSV files
children = pd.read_csv("{0}\Children.csv".format(CSVLocation), skiprows=1,
            names=["email","name","subject",
                   "contactAmount","meetingPlaces",
                   "arts","sports","entertainment","nightOut"],
            usecols=range(1,10))

# Add ID columns to both Pandas
parents.insert(0, "ID", range(0,len(parents)))
children.insert(0, "ID", range(0,len(children)))

###################################################

################# Pandas are setup and ready, structure shown below #################

# Parents : ID, email, name1, name2, name3, yearGoingInto, childrenAlready, subjects,
#           contactAmount, meetingPlaces, arts, sports, entertainment, nightOut

# Children: ID, email, name, subject, contactAmount, meetingPlaces, arts, sports,
#           entertainment, nightOut

#####################################################################################



############### Forming Allocation Data Structure ###############

#row = parents.loc[0]
#email = row["email"]

# Allocation stored in
allocation = []

#################################################################



###############  ###############
