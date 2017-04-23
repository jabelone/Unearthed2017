import os, csv, pickle

# Get the current working directory and all files
mypath = os.getcwd()
files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

# Store our sanitised and combined csv
sanitisedCSV = [{}]
combinedCSV = [{}]
SVMstring = ""
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
            iteration += 1

            #sanitisedCSV.append({})
            #sanitisedCSV[iteration]["Well"] = currentWell
            #sanitisedCSV[iteration]["Downhole Gauge Pressure"] = row["Downhole Gauge Pressure"]
            #sanitisedCSV[iteration]["Casing Pressure"] = row["Casing Pressure"]
            #sanitisedCSV[iteration]["Gas Flow (Volume)"] = row["Gas Flow (Volume)"]
            #sanitisedCSV[iteration]["Motor Speed"] = row["Motor Speed"]
            #sanitisedCSV[iteration]["Motor Torque"] = row["Motor Torque"]
            #sanitisedCSV[iteration]["Pump Speed Actual"] = row["Pump Speed Actual"]
            #sanitisedCSV[iteration]["Tubing Flow Meter"] = row["Tubing Flow Meter"]
            #sanitisedCSV[iteration]["Tubing Pressure"] = row["Tubing Pressure"]
            #sanitisedCSV[iteration]["Tubing Size Type"] = row["Tubing Size Type"]
            #sanitisedCSV[iteration]["Water Flow Mag from Separator"] = row["Water Flow Mag from Separator"]

            sanitisedCSV.append({})
            s = {}
            s[0] = currentWell
            s[1] = row["Downhole Gauge Pressure"]
            s[2] = row["Casing Pressure"]
            s[3] = row["Gas Flow (Volume)"]
            s[4] = row["Motor Speed"]
            s[5] = row["Motor Torque"]
            s[6] = row["Pump Speed Actual"]
            s[7] = row["Tubing Flow Meter"]
            s[8] = row["Tubing Pressure"]
            #s[9] = row["Tubing Size Type"]
            s[10] = row["Water Flow Mag from Separator"]

            if "NULL" in s.values():
                nulls += 1
                continue

            sanitisedCSV.append(s)

            rowString = "{} 1:{} 2:{} 3:{} 4:{} 5:{} 6:{} 7:{} 8:{}\n".\
                format(row["Downhole Gauge Pressure"], row["Casing Pressure"], row["Gas Flow (Volume)"],
                       row["Motor Speed"], row["Motor Torque"], row["Pump Speed Actual"], row["Tubing Flow Meter"],
                       row["Tubing Pressure"], row["Water Flow Mag from Separator"])
            SVMstring += rowString
        print("Found {} nulls in the dataset.  I have purged the unwanted.".format(nulls))

print("There was {} nulls in all of the datasets.  I have purged the unwanted.".format(nulls))
print(SVMstring[:500])

SVMfile = open("svmTrain.txt", 'w')
SVMfile.write(SVMstring)
SVMfile.close()

with open("sanitisedData.txt", "wb") as dataFile:
    pickle.dump(sanitisedCSV, dataFile)