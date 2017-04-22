import os, csv, pickle

# Get the current working directory and all files
mypath = os.getcwd()
files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

# Store our sanitised and combined csv
sanitisedCSV = [{}]
combinedCSV = [{}]
iteration = 0
nulls = 0

# Pop all the non csv files
for index, name in enumerate(files):
    if ".csv" in name:
        pass
    else:
        files.pop(index)
print("Will combine all these ({} in total): ".format(len(files)))
print(files)
print("\n")

for i, dataset in enumerate(files):
    with open(dataset) as file:
        # Read the current file into a variable
        reader = csv.DictReader(file)

        currentWell = files[i][4:6]

        print("Working on {} of {}".format(i, len(files)))
        print("Processing well: ")
        print(currentWell)

        for index, row in enumerate(reader):
            if "NULL" in row:
                nulls += 1
                continue
            sanitisedCSV.append({})
            sanitisedCSV[index]["Well"] = currentWell
            sanitisedCSV[index]["Downhole Gauge Pressure"] = row["Downhole Gauge Pressure"]
            sanitisedCSV[index]["Casing Pressure"] = row["Casing Pressure"]
            sanitisedCSV[index]["Gas Flow (Volume)"] = row["Gas Flow (Volume)"]
            sanitisedCSV[index]["Motor Speed"] = row["Motor Speed"]
            sanitisedCSV[index]["Motor Torque"] = row["Motor Torque"]
            sanitisedCSV[index]["Pump Speed Actual"] = row["Pump Speed Actual"]
            sanitisedCSV[index]["Tubing Flow Meter"] = row["Tubing Flow Meter"]
            sanitisedCSV[index]["Tubing Pressure"] = row["Tubing Pressure"]
            sanitisedCSV[index]["Tubing Size Type"] = row["Tubing Size Type"]
            sanitisedCSV[index]["Water Flow Mag from Separator"] = row["Water Flow Mag from Separator"]

        print("Found {} nulls in this dataset.  I have purged the unwanted.".format(nulls))

print("There was {} nulls in all of the datasets.  I have purged the unwanted.".format(nulls))
with open("sanitisedData.txt", "wb") as dataFile:
    pickle.dump(sanitisedCSV, dataFile)