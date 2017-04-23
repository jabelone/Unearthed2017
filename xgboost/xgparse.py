import pickle
print("loading...\n")
trainingData = pickle.load(open("sanitisedData.txt", "rb"))
testData = pickle.load(open("sanitisedTestData.txt", "rb"))

print("Stuff: ")
print(trainingData[1])

