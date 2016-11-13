import unittest

from my_fpgrowth import (
    sort_transactions,
    build_fp_tree,
    build_nominal_tree,
    find_common_sets
)

class FpGrowthTests(unittest.TestCase):

  def test_transactions_are_sorted_correctly(self):
      goods = dict()
      goods[tuple([3])] = 0.8
      goods[tuple([1])] = 0.5
      goods[tuple([2])] = 0.45
      goods[tuple([4])] = 0.1
      transactions = [[], [0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1, 1], [1, 1, 0, 1, 0]]
      expectedResult = [[], [2, 3, 1, 4], [], [3, 1]]
      numTransactions = len(transactions)
      result = sort_transactions(transactions, goods.items())
      for i in range(numTransactions):
          self.assertEquals(result[i], expectedResult[i])
      return

  def test_fp_tree_is_builded_correctly(self):
      return

  def test_all_common_sets_are_founded(self):
      return

  def nominal_fp_tree_is_builded_correctly(self):
      return

if __name__ == '__main__':
    unittest.main()