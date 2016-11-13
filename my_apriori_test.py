import unittest

from candidates_func import (
    remove_excess_sets,
    candidates_generation,
    is_subset,
    count_candidates_support,
    get_proper_set
)

class AprioriTests(unittest.TestCase):

  def test_candidates_support_is_counted_correctly(self):
      data = [[1, 0, 0, 1, 0, 1, 0], [1, 0, 1, 0, 0, 0, 0], [1, 0, 0, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]]
      candidates = [[], [0], [1, 3], [2, 4, 5, 6], [4, 5, 6], [10]]
      expectedSupport = [1, 1, 0.25, 0.25, 0.5, 0]
      numCandidates = len(candidates)
      candidatesWithSupport = count_candidates_support(candidates, data, len(data))
      for i in range(numCandidates):
          self.assertEquals(candidatesWithSupport[tuple(candidates[i])], expectedSupport[i])
      return

  def test_only_sets_with_support_bigger_then_min_support_are_used(self):
      minSupport = 0.42
      candidateSet = dict()
      candidateSet[tuple([1, 5])] = 0.6
      candidateSet[tuple([1, 6, 9])] = 0.42
      candidateSet[tuple([0, 8])] = 0.41
      candidateSet[tuple([17, 8, 25])] = 0
      expectedResult = dict()
      expectedResult[tuple([1, 5])] = 0.6
      expectedResult[tuple([1, 6, 9])] = 0.42
      get_proper_set(candidateSet, minSupport)
      self.assertEquals(expectedResult, candidateSet)

  def test_new_candidates_are_found_correctly(self):
      previousCommonGoods = dict()
      numberOfGoods = 4
      expectedResult = []
      result = candidates_generation(previousCommonGoods.keys(), numberOfGoods)
      self.assertEquals(result, expectedResult)

      previousCommonGoods[tuple([0])] = 0.3
      expectedResult = []
      result = candidates_generation(previousCommonGoods.keys(), numberOfGoods)
      self.assertEquals(result, expectedResult)

      previousCommonGoods[tuple([1])] = 0.4
      previousCommonGoods[tuple([2])] = 0.12
      previousCommonGoods[tuple([3])] = 0.94
      expectedResult = [[2, 3], [0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]
      result = candidates_generation(previousCommonGoods.keys(), numberOfGoods)
      self.assertEquals(result, expectedResult)

  def test_candidate_set_contains_only_sets_with_subsets_in_previous_common_set(self):
      previousCommonGoods = dict()
      numberOfGoods = 4
      previousCommonGoods[tuple([0])] = 0.3
      previousCommonGoods[tuple([2])] = 0.12
      previousCommonGoods[tuple([3])] = 0.94
      expectedResult = [[2, 3], [0, 2], [0, 3]]
      result = candidates_generation(previousCommonGoods.keys(), numberOfGoods)
      self.assertEquals(result, expectedResult)

  def test_all_excess_sets_are_removed(self):
      previousCommonGoods = dict()
      previousCommonGoods[tuple([0])] = 0.3
      previousCommonGoods[tuple([2])] = 0.12
      previousCommonGoods[tuple([3])] = 0.94
      candidates = [[2, 3], [0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]
      expectedResult = [[2, 3], [0, 2], [0, 3]]
      result = remove_excess_sets(candidates, previousCommonGoods.keys())
      self.assertEquals(result, expectedResult)

      del previousCommonGoods[tuple([2])]
      del previousCommonGoods[tuple([0])]
      expectedResult = []
      result = remove_excess_sets(candidates, previousCommonGoods.keys())
      self.assertEquals(result, expectedResult)

  def test_checking_if_set_is_subset_works_corerectly(self):
      set = [1, 0, 1, 0, 1, 0, 0, 0, 0]
      subset = []
      subset.append([])
      subset.append([1])
      subset.append([2, 4])
      subset.append([0, 2, 4])
      subset.append([2, 10])
      expectedResult = [True, False, True, True, False]
      numSets = len(subset)
      for i in range(numSets):
          result = is_subset(subset[i], set)
          self.assertEquals(result, expectedResult[i])
      return

if __name__ == '__main__':
    unittest.main()