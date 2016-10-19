import sys
import numpy as np

def parse_csv_dataset(fileName):
    dataSet = []
    with open(fileName, 'rb') as csvfile:
        for line in csvfile.readlines():
            rowAsString = line.split(',')
            rowAsString = np.delete(rowAsString, np.s_[0:1], axis=0)
            numElements = rowAsString.size
            rowAsInt = []
            for i in range(numElements):
                rowAsInt.append(int(rowAsString[i]))
            dataSet.append(rowAsInt)
    return dataSet

def remove_excess_rules(candidateSet):
    betterCandidateSet = []

    return betterCandidateSet

def candidates_generation(previousCandidateSet):
    newCandidates = []

    newCandidates = remove_excess_rules(newCandidates)
    return newCandidates

dataFileName = sys.argv[1]
data = parse_csv_dataset(dataFileName)

numTransactions = len(data)
numGoods = len(data[0])
singletonSet = []

for i in range(numGoods):
    singletonSet.append(i)

commonRules = []
candidates = candidates_generation(commonRules)


