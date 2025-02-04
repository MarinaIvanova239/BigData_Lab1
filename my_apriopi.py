import sys
import common
import time
import candidates_func

def run_apriori(commonGoodsSet, numGoods, data, numTransactions, minSupport):
    arrayOfCommonSets = []
    while commonGoodsSet:
        arrayOfCommonSets.append(commonGoodsSet)
        candidateSet = candidates_func.candidates_generation(commonGoodsSet.keys(), numGoods)
        commonGoodsSet = candidates_func.count_candidates_support(candidateSet, data, numTransactions)
        candidates_func.get_proper_set(commonGoodsSet, minSupport)

    return arrayOfCommonSets

if __name__ == "__main__":

    startTime = time.time()

    dataFileName = sys.argv[1]
    minSupport = float(sys.argv[2])
    minConf = float(sys.argv[3])

    if minSupport > 1 or minSupport < 0:
        print 'MinSupport must be in [0, 1]'
        quit()
    if minConf > 1 or minConf < 0:
        print 'MinConf must be in [0, 1]'
        quit()

    # read transactions from csv file
    data = common.get_dataset_from_csv_file(dataFileName)
    numTransactions = len(data)
    numGoods = 0
    if data:
        numGoods = len(data[0])

    # count support of each good
    commonGoodsSet = dict()
    common.count_good_support(data, numTransactions, commonGoodsSet, numGoods)
    for i in range(numGoods):
        if commonGoodsSet[tuple([i])] < minSupport:
            del commonGoodsSet[tuple([i])]

    # run apriori - find all sets of common goods (which have support more than minSupport)
    arrayOfCommonSets = run_apriori(commonGoodsSet, numGoods, data, numTransactions, minSupport)

    # find common rules from common sets (confidence more than minConf)
    commonRules = dict()
    numCommonSets = len(arrayOfCommonSets)
    for i in range(1, numCommonSets):
        commonSetItems = arrayOfCommonSets[i].items()
        for key, value in commonSetItems:
            common.get_common_rules(commonRules, arrayOfCommonSets, list(key), value, minConf, list(key))

    endTime = time.time()

    # print results
    print 'items:'
    for commonSet in arrayOfCommonSets:
        for element, support in commonSet.items():
            print element, ':', support

    print '.......'
    print 'rules:'
    for eachRule, conf in commonRules.items():
        print eachRule, ':', conf

    print '.......'
    print 'time=', endTime - startTime


