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

def candidates_generation(previousCandidateSet, numIteration):

    newCandidates = []
    sizeOfPreviousCandidateSet = len(previousCandidateSet)
    index = 0
    for i in range(sizeOfPreviousCandidateSet):
        for j in range(i, sizeOfPreviousCandidateSet - 1):
            newCandidates.append(previousCandidateSet[i])
            newCandidates[index].append(previousCandidateSet[j][numIteration - 1])
            index = index + 1

    newCandidates = remove_excess_rules(newCandidates)
    return newCandidates

def get_proper_set(commonRules):

    properSet = []
    return properSet

dataFileName = sys.argv[1]
data = parse_csv_dataset(dataFileName)

numTransactions = len(data)
numGoods = len(data[0])
candidateSet = []
for i in range(numGoods):
    singletonSet = []
    singletonSet.append(i)
    candidateSet.append(singletonSet)

commonRules = []
for k in range(1):
    commonRules = candidates_generation(candidateSet, k + 1)
    candidateSet = get_proper_set(commonRules)

