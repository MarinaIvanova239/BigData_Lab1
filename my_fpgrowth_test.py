import unittest
import operator

from my_fpgrowth import (
    sort_transactions,
    build_fp_tree,
    build_nominal_tree,
    run_fpgrowth,
    Tree
)

from common import (
    count_good_support
)

class FpGrowthTests(unittest.TestCase):

  def test_transactions_are_sorted_correctly(self):
      goods = dict()
      goods[tuple([3])] = 0.8
      goods[tuple([1])] = 0.5
      goods[tuple([2])] = 0.45
      goods[tuple([4])] = 0.1
      sortedGoods = sorted(goods.items(), key=operator.itemgetter(1), reverse=True)
      transactions = [[], [0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1, 1], [1, 1, 0, 1, 0]]
      expectedResult = [[], [3, 1, 2, 4], [], [3, 1]]
      numTransactions = len(transactions)
      result = sort_transactions(transactions, sortedGoods)
      for i in range(numTransactions):
          self.assertEquals(result[i], expectedResult[i])
      return

  def test_fp_tree_is_builded_correctly(self):
      transactions = [[1, 2, 3, 4], [6, 3, 4, 1], [1, 4, 0], [6, 3, 5], [5]]
      numGoods = 7
      fpTree = Tree(numGoods)
      build_fp_tree(fpTree, transactions)
      rootChildren = []
      numChildrenOne = -1
      numChildrenSix = -1
      numChildrenFive = -1
      for child in fpTree.root.children:
          rootChildren.append(child.name)
          if child.name == 1:
              numChildrenOne = len(child.children)
          elif child.name == 6:
              numChildrenSix = len(child.children)
          elif child.name == 5:
              numChildrenFive = len(child.children)
      self.assertEquals(rootChildren, [1, 6, 5])
      self.assertEquals(numChildrenOne, 2)
      self.assertEquals(numChildrenSix, 1)
      self.assertEquals(numChildrenFive, 0)
      self.assertEquals(fpTree.goodSupport[tuple([6])], 2)
      return

  def test_all_common_sets_are_founded(self):
      minSupport = 0.5
      transactions = [[0, 1, 1, 1, 1, 0, 0], [0, 1, 0, 1, 1, 0, 1], [1, 1, 0, 0, 1, 0, 0],
                      [0, 0, 0, 1, 0, 1, 1], [0, 0, 0, 0, 1, 0, 0]]
      numGoods = 7
      goods = dict()
      count_good_support(transactions, len(transactions), goods, numGoods)
      for i in range(numGoods):
          if goods[tuple([i])] < minSupport:
              del goods[tuple([i])]

      result = run_fpgrowth(goods, transactions, numGoods, len(transactions), minSupport)

      commonSetsOneElem = dict()
      commonSetsOneElem[tuple([1])] = 0.6
      commonSetsOneElem[tuple([3])] = 0.6
      commonSetsOneElem[tuple([4])] = 0.8

      commonSetsTwoElem = dict()
      commonSetsTwoElem[tuple([1, 4])] = 0.6

      expectedResult = []
      expectedResult.append(commonSetsOneElem)
      expectedResult.append(commonSetsTwoElem)
      self.assertEquals(result, expectedResult)

  def test_nominal_fp_tree_is_builded_correctly(self):
      transactions = [[1, 2, 3, 4], [6, 3, 4, 1], [1, 4, 0], [6, 3, 5], [5]]
      numGoods = 7
      fpTree = Tree(numGoods)
      build_fp_tree(fpTree, transactions)
      nominalTree = build_nominal_tree(fpTree, 4)
      rootChildren = []
      numChildrenOne = -1
      numChildrenSix = -1
      for child in nominalTree.root.children:
          rootChildren.append(child.name)
          if child.name == 1:
              numChildrenOne = len(child.children)
          elif child.name == 6:
              numChildrenSix = len(child.children)
      self.assertEquals(rootChildren, [1, 6])
      self.assertEquals(numChildrenOne, 2)
      self.assertEquals(numChildrenSix, 1)
      self.assertEquals(nominalTree.goodSupport[tuple([6])], 1)
      return

if __name__ == '__main__':
    unittest.main()