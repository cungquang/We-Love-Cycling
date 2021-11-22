import pandas as pd

# format and clean elevation data
def elevationData(filename):
    if filename.endswith("\n"):
        filename = filename[:-1]
        
    if filename.endswith('.csv'):
        ride = pd.read_csv(filename)
        lastElevation = ride['alt'][0]
        elevationGain = 0
        for index, row in ride.iterrows():
            if row['alt'] > lastElevation:
                elevationGain += (row['alt'] - lastElevation)
            elif row['alt'] < lastElevation:
                elevationGain += 0
            else:
                elevationGain += 0
            lastElevation = row['alt']
        if ride['km'].iloc[-1] != 0:
            s_index = elevationGain / ride['km'].iloc[-1]
            return s_index
        else:
            return -1

# get slope
def slope(lastDistance, currDistance, lastAltitude, currAltitude):
    if currDistance == lastDistance:
        return 0
    else:
        #altitude is in m
        #distance is in km, therefore we divide by 1000
        #then we multiply by 100 to convert the grade to a percentage
        #which is why it ends up being divided by 10
        s = ((currAltitude - lastAltitude)/(currDistance - lastDistance))/10
        return s

# get s_index
def elevationIndex(filename, distanceInterval):
    if filename.endswith("\n"):
        filename = filename[:-1]
        
    if filename.endswith('.csv'):
        ride = pd.read_csv(filename)
        currInterval = ride['km'][0]
        lastDistance = ride['km'][0]
        lastAltitude = ride['alt'][0]
        slopeValues = []
        
        for index, row in ride.iterrows():
            if currInterval >= distanceInterval:
                #slopeValues.append(slope for this section)
                slopeValues.append(slope(lastDistance, row['km'], lastAltitude, row['alt']))
                #reset currInterval to 0
                currInterval = 0
                #set lastAltitude to current altitude
                lastAltitude = row['alt']
                #set lastDistance to current distance
                lastDistance = row['km']
            else:
                currInterval += row['km']
    return slopeValues

