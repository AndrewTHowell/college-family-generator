### College Family Generator

import pandas as pd

parents = pd.read_csv("Test Data\Parents.csv", skiprows=1,
            names=["email","name1","name2","name3","yearGoingInto","childrenAlready","subjects",
                   "contactAmount","meetingPlaces",
                   "arts","sports","entertainment","nightOut"],
            usecols=range(1,14))

children = pd.read_csv("Test Data\Children.csv", skiprows=1,
            names=["email","name","subjects",
                   "contactAmount","meetingPlaces",
                   "arts","sports","entertainment","nightOut"],
            usecols=range(1,10))

print(parents.iloc[0]["email"])

