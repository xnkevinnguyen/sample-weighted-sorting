import unittest

from .mock_data import FakeData
from .utility import ItemSortManager


# Create your tests here.

class UtilityTest(unittest.TestCase):
    CONST_ITEM_NUMBER = 100
    fake_data = FakeData()

    # Returns True or False.
    def test_item_order(self):
        """
        Asserts that the class ItemSortManager returns an ordered list with descending
        order of estimated value
        """
        unordered_item_list = self.fake_data.get_unordered_item_list(self.CONST_ITEM_NUMBER)

        item_sort_manager = ItemSortManager(unordered_item_list, self.fake_data.price_weight,
                                            self.fake_data.recency_weight,
                                            self.fake_data.popularity_weight)

        sorted_items = item_sort_manager.get_sorted_items()

        # iterate through the sorted last up to before last
        is_value_descending = True

        for i in range(0, self.CONST_ITEM_NUMBER - 2):
            if sorted_items[i]['estimated_value'] < sorted_items[i + 1]['estimated_value']:
                is_value_descending = False
            break

        self.assertTrue(is_value_descending)


if __name__ == '__main__':
    unittest.main()
