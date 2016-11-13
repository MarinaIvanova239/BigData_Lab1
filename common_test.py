import unittest
import os
import csv

from common import (
    get_dataset_from_csv_file,
    count_good_support,
    get_subsets,
    find_rest_part,
    get_common_rules
)

class CommonTests(unittest.TestCase):

    def test_csv_file_is_parsed_correctly(self):
        fileName = 'apriori_test.csv'
        with open(fileName, 'w') as fp:
            a = csv.writer(fp, delimiter=',')
            data = [['1', '0', '0', '0'],
                    ['2', '0', '1', '0'],
                    ['3', '1', '1', '1']]
            a.writerows(data)
        data = get_dataset_from_csv_file(fileName)
        expectedData = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
        self.assertEquals(data, expectedData)
        os.system('del ' + fileName)
        return

    def test_empty_list_if_there_are_no_input_transactions(self):
        fileName = 'apriori_test.csv'
        os.system('copy nul > ' + fileName)
        data = get_dataset_from_csv_file(fileName)
        expectedData = [[]]
        self.assertEquals(data, expectedData)
        os.system('del ' + fileName)

    def test_support_for_each_good_is_counted_correctly(self):
        set = []
        set.append([[]])
        set.append([[1, 1, 1, 1]])
        set.append([[1, 1, 1, 1], [1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 1, 1]])
        expectedSupport = [0, 1, 0.5]

        numSets = len(set)
        good = 2
        for i in range(numSets):
            support = count_good_support(good, set[i], len(set[i]))
            self.assertEquals(support, expectedSupport[i])

    def test_all_subsets_of_set_are_founded(self):
        set = []
        expectedSubset = []
        set.append([1])
        set.append([1, 2])
        set.append([1, 2, 3])
        expectedSubset.append([[]])
        expectedSubset.append([[1], [2]])
        expectedSubset.append([[1, 2], [2, 3], [1, 3]])
        numSets = len(set)
        for i in range(numSets):
            resultSubset = get_subsets(set[i])
            self.assertEquals(resultSubset, expectedSubset[i])

        sizeBigSet = 100
        bigSet = []
        for i in range(sizeBigSet):
            bigSet.append(i)
        resultSubset = get_subsets(bigSet)
        self.assertEquals(sizeBigSet, len(resultSubset))
        self.assertEquals(sizeBigSet - 1, len(resultSubset[0]))
        return

    def rest_part_of_subset_is_found_correctly(self):
        set = [1, 2, 3, 4, 5, 6, 7, 8]
        subset = []
        expectedRestPart = []
        subset.append([])
        subset.append([1])
        subset.append([2, 5])
        subset.append([1, 2, 3, 4, 5, 6, 7, 8])
        expectedRestPart.append([1, 2, 3, 4, 5, 6, 7, 8])
        expectedRestPart.append([2, 3, 4, 5, 6, 7, 8])
        expectedRestPart.append([1, 3, 4, 6, 7, 8])

        numSets = len(set)
        for i in range(numSets):
            restPart = find_rest_part(subset[i], set)
            self.assertEquals(restPart, expectedRestPart[i])

    def test_common_rules_are_counted_correctly(self):
        commonSetsOneElem = dict()
        commonSetsOneElem[tuple([0])] = 0.96
        commonSetsOneElem[tuple([1])] = 0.75
        commonSetsOneElem[tuple([2])] = 0.69

        commonSetsTwoElem = dict()
        commonSetsTwoElem[tuple([0, 2])] = 0.43
        commonSetsTwoElem[tuple([1, 2])] = 0.5
        commonSetsTwoElem[tuple([0, 1])] = 0.46

        commonSetsThreeElem = dict()
        commonSetsThreeElem[tuple([0, 1, 2])] = 0.22

        commonSets = []
        commonSets.append(commonSetsOneElem)
        commonSets.append(commonSetsTwoElem)

        expectedCommonRules = dict()
        expectedCommonRules[(tuple([2]), tuple([0]))] = commonSetsTwoElem[tuple([0, 2])] / commonSetsOneElem[tuple([2])]
        expectedCommonRules[(tuple([1]), tuple([2]))] = commonSetsTwoElem[tuple([1, 2])] / commonSetsOneElem[tuple([1])]
        expectedCommonRules[(tuple([2]), tuple([1]))] = commonSetsTwoElem[tuple([1, 2])] / commonSetsOneElem[tuple([2])]
        expectedCommonRules[(tuple([1]), tuple([0]))] = commonSetsTwoElem[tuple([0, 1])] / commonSetsOneElem[tuple([1])]

        minConf = 0.5
        commonRules = dict()
        numCommonSets = len(commonSets)
        for i in range(1, numCommonSets):
            commonSetItems = commonSets[i].items()
            for key, value in commonSetItems:
                get_common_rules(commonRules, commonSets, list(key), value, minConf, list(key))

        self.assertEquals(commonRules, expectedCommonRules)

        commonSets.append(commonSetsThreeElem)
        expectedCommonRules[(tuple([0, 2]), tuple([1]))] = commonSetsThreeElem[tuple([0, 1, 2])] / commonSetsTwoElem[tuple([0, 2])]

        commonRules = dict()
        numCommonSets = len(commonSets)
        for i in range(1, numCommonSets):
            commonSetItems = commonSets[i].items()
            for key, value in commonSetItems:
                get_common_rules(commonRules, commonSets, list(key), value, minConf, list(key))

        self.assertEquals(commonRules, expectedCommonRules)


if __name__ == '__main__':
    unittest.main()