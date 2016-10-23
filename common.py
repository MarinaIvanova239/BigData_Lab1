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

def count_good_support(good, transactions, numberOfTransactions):

    transactionsWithGood = 0
    for eachTransaction in transactions:
        if eachTransaction[good] > 0:
            transactionsWithGood = transactionsWithGood + 1

    goodSupport = transactionsWithGood / float(numberOfTransactions)
    return goodSupport