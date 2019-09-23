import math
from datetime import datetime
import numpy as np
from collections import OrderedDict


# CONST_AVERAGE = 100


class ItemSortManager:
    CONST_AVERAGE = 100
    CONST_SPREAD_FACTOR = 0.04
    CURRENT_TIME = int(datetime.now().strftime('%m%d%H'))

    def __init__(self, store_items, price_weight=0, recency_weight=0, popularity_weight=0):
        """Constructor of a value calculator for a list of store items"""

        self.__price_weight = price_weight
        self.__recency_weight = recency_weight
        self.__popularity_weight = popularity_weight

        print("Initializing averages and Standard Deviations for current item list")

        price_list = [item.price for item in store_items]
        recency_list = [self.CURRENT_TIME - int(item.created_on.strftime('%m%d%H')) for item in store_items]
        popularity_list = [item.popularity for item in store_items]

        self.__price = {
            'weight':price_weight,
            'contribution_coefficient':-1,
            'average': np.mean(price_list),
            'standard_deviation': math.sqrt(np.var(price_list))
        }
        self.__popularity = {
            'weight':popularity_weight,
            'contribution_coefficient': 1,
            'average': np.mean(popularity_list),
            'standard_deviation': math.sqrt(np.var(popularity_list))
        }
        self.__recency = {
            'weight':recency_weight,
            'contribution_coefficient': -1,
            'average': np.mean(recency_list),
            'standard_deviation': math.sqrt(np.var(recency_list))
        }

        self.__criterias = OrderedDict([('price',self.__price),('popularity', self.__popularity), ('time_since_posted',self.__recency)])

        print("Calling Sorting algorithm")

        self.__sorted_items = self.sort_by_estimated_value(store_items)

    def get_sorted_items(self):
        return self.__sorted_items

    def sort_by_estimated_value(self, storeitems):
        """Quick sort implementation, average case of O(nLogn)"""
        sorted_items = []
        for item in storeitems:
            estimated_value = self.get_estimated_value(item)
            valued_item = {
                'store_item': item.get(),
                'estimated_value': estimated_value
            }

            sorted_items.append(valued_item)
        self.quick_sort(sorted_items, 0, len(sorted_items) - 1)
        return sorted_items

    def get_estimated_value(self, store_item) -> int:
        """Returns the estimated value of the item according to the criterias """
        estimated_value = self.CONST_AVERAGE
        # Having a higher price reduces the value
        print("Calculating ETV")
        store_item.time_since_posted=self.CURRENT_TIME - int(store_item.created_on.strftime('%m%d%H'))

        for  criteria_key,criteria in self.__criterias.items():
            print(criteria_key +str(getattr(store_item,criteria_key)))
            estimated_value += self.CONST_SPREAD_FACTOR *criteria['contribution_coefficient']\
                *criteria['weight']*(getattr(store_item,criteria_key)-criteria['average'])/criteria['standard_deviation']


        # estimated_value -= self.CONST_SPREAD_FACTOR * self.__price_weight * (
        #         store_item.price - self.__price['average']) / self.__price['standard_deviation']
        #
        # # Higher time since posted reduces the value
        # date_time_value = int(store_item.created_on.strftime('%m%d%H'))
        # time_since_posted = self.CURRENT_TIME - date_time_value
        # estimated_value -= self.CONST_SPREAD_FACTOR * self.__recency_weight * (
        #         time_since_posted - self.__recency['average']) / self.__recency['standard_deviation']
        #
        # # Having a high popularity  increases the value
        # estimated_value += self.CONST_SPREAD_FACTOR * self.__popularity_weight * (
        #         store_item.popularity - self.__popularity['average']) / self.__popularity['standard_deviation']

        return int(estimated_value)

    def quick_sort(self, list, startindex, endindex):
        """Recursive function to separate partitions to sort"""
        # TODO Make Static

        initial_pivot_value = self.get_initial_pivot(list, startindex, endindex)

        self.quick_sort_helper(list, startindex, endindex, initial_pivot_value)

    def quick_sort_helper(self, list, startindex, endindex, pivotvalue):
        """Recursive function to separate partitions to sort"""
        # TODO Make Static

        if startindex < endindex:
            new_center_index = partition(list, startindex, endindex, pivotvalue)

            # item a center index is now at the right partition
            left_pivot = get_set_pivot(list, startindex, new_center_index - 1)
            self.quick_sort_helper(list, startindex, new_center_index - 1, left_pivot)

            if (new_center_index + 1) <= endindex:
                right_pivot = get_set_pivot(list, new_center_index + 1, endindex)
                self.quick_sort_helper(list, new_center_index + 1, endindex, right_pivot)

    def get_initial_pivot(self, item_list, start_index, end_index):
        """Returns the value closest to the const average"""
        # TODO Make Static
        if (end_index - start_index) > 2:
            middle_index = int((start_index + end_index) / 2)
            start_difference = abs(self.CONST_AVERAGE - item_list[start_index]['estimated_value'])

            middle_difference = abs(self.CONST_AVERAGE - item_list[middle_index]['estimated_value'])
            end_difference = abs(self.CONST_AVERAGE - item_list[end_index]['estimated_value'])
            if end_difference <= middle_difference & end_difference <= start_difference:
                item_list[start_index], item_list[end_index] = item_list[end_index], item_list[start_index]

            if middle_difference <= start_difference & middle_difference <= end_difference:
                item_list[start_index], item_list[middle_index] = item_list[middle_index], item_list[start_index]

        return item_list[start_index]['estimated_value']


def partition(list, start_index, end_index, pivot_value):
    """Handles putting the pivot at right position and distribute smaller then pivot to the left
            and bigger element to the right
            """
    border_index = start_index + 1

    for i in range(border_index, end_index + 1):

        if list[i]['estimated_value'] >= pivot_value:
            list[i], list[border_index] = list[border_index], list[i]

            border_index += 1

    pivot_index = border_index - 1
    list[start_index], list[pivot_index] = list[pivot_index], list[start_index]
    return pivot_index


def get_set_pivot(item_list, start_index, end_index):
    """
    Returns the median of 3 values  start, middle and end of the list
    Sets the pivot at startindex position of the list
    """
    # TODO Refactor
    if (end_index - start_index) > 2:
        middle_index = int((start_index + end_index) / 2)
        if ((item_list[start_index]['estimated_value'] <= item_list[middle_index]['estimated_value']) &
                (item_list[middle_index]['estimated_value'] <= item_list[end_index]['estimated_value']) | (
                        item_list[end_index]['estimated_value'] <= item_list[middle_index]['estimated_value']) &
                (item_list[middle_index]['estimated_value'] <= item_list[start_index]['estimated_value'])):
            item_list[start_index], item_list[middle_index] = item_list[middle_index], item_list[start_index]
            return item_list[start_index]['estimated_value']
        if ((item_list[middle_index]['estimated_value'] <= item_list[start_index]['estimated_value']) &
                (item_list[start_index]['estimated_value'] <= item_list[end_index]['estimated_value']) | (
                        item_list[end_index]['estimated_value'] <= item_list[start_index]['estimated_value']) &
                (item_list[start_index]['estimated_value'] <= item_list[middle_index]['estimated_value'])):
            return item_list[start_index]['estimated_value']
        else:
            item_list[start_index], item_list[end_index] = item_list[end_index], item_list[start_index]
            return item_list[start_index]['estimated_value']

    else:

        return item_list[start_index]['estimated_value']
