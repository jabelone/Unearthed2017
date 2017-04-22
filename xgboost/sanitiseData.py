import os
import random
from shutil import copyfile

totalFiles = 0

fileNames = os.listdir(os.getcwd())
stringOfFiles = ""
iteration = 0

if not os.path.exists("randomly_sorted"):
    os.makedirs("randomly_sorted")

for file in fileNames:
    if file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".png") or file.endswith(".PNG"):
        filteredFileNames.append(file)
        if os.path.exists("randomly_sorted/" + file):
            os.remove("randomly_sorted/" + file)

        if not os.path.exists("randomly_sorted/" + file + "_temp"):
            copyfile(file, "randomly_sorted/" + file + "_temp")
        else:
            os.remove("randomly_sorted/" + file + "_temp")
            copyfile(file, "randomly_sorted/" + file + "_temp")

values = list(range(len(filteredFileNames)))
random.shuffle(values)

for file in filteredFileNames:
    file += ", "
    stringOfFiles += file
    newNames[file] = iteration
    iteration += 1

print("These files will be randomised: " + stringOfFiles)
print("The total files to randomise is: " + str(len(filteredFileNames)))
iteration = 0

for file in filteredFileNames:
    if os.path.exists("randomly_sorted/" + file):
        os.remove("randomly_sorted/" + file)
    if os.path.exists("randomly_sorted/" + str(values[iteration]) + ".jpg"):
        os.remove("randomly_sorted/" + str(values[iteration]) + ".jpg")

    os.rename("randomly_sorted/" + file + "_temp", "randomly_sorted/" + str(values[iteration]) + ".jpg")
    iteration += 1