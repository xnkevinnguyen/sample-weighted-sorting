import math
from datetime import datetime


class ItemSortManager:
    CONST_AVERAGE = 100
    CONST_SPREAD_FACTOR = 7
    CURRENT_TIME = int(datetime.now().strftime('%m%d%H'))

    def __init__(self, storeitems, priceweight=0, recencyweight=0, popularityweight=0):
        """Constructor of a value calculator for a list of store items"""

        self.__price_weight = priceweight
        self.__recency_weight = recencyweight
        self.__popularity_weight = popularityweight


        sum = {
            'price': 0,
            'popularity': 0,
            'recency': 0
        }
        variance_sum = {
            'price': 0,
            'popularity': 0,
            'recency': 0
        }
        items_quantity = len(storeitems)

        for item in storeitems:
            if item.price:
                sum['price'] += item.price
                variance_sum['price'] += math.pow(item.price, 2)
            if item.popularity:
                sum['popularity'] += item.popularity
                variance_sum['popularity'] += math.pow(item.popularity, 2)
            if item.created_on:
                date_time_value = int(item.created_on.strftime('%m%d%H'))
                time_since_posted = self.CURRENT_TIME - date_time_value
                sum['recency'] += time_since_posted
                variance_sum['recency'] += math.pow(time_since_posted, 2)
        variance_divider = items_quantity - 1
        self.__price = {
            'average': sum['price'] / items_quantity,
            'variance': variance_sum['price'] / (variance_divider)
        }
        self.__popularity = {
            'average': sum['popularity'] / items_quantity,
            'variance': variance_sum['popularity'] / (variance_divider)
        }
        self.__recency = {
            'average': sum['recency'] / items_quantity,
            'variance': variance_sum['recency'] / (variance_divider)
        }

        self.__sorted_items = self.sort_by_estimated_value(storeitems)

    def get_sorted_items(self):
        return self.__sorted_items

    def sort_by_estimated_value(self, storeitems):
        """Quick sort implementation, average case of O(nLogn)"""
        sorted_items = []
        for item in storeitems:
            random_value = self.get_estimated_value(item)
            valued_item = {
                'store_item': item.get(),
                'estimated_value': random_value
            }

            sorted_items.append(valued_item)
        self.quick_sort(sorted_items, 0, len(sorted_items) - 1)
        return sorted_items

    def get_estimated_value(self, storeitem):
        """Returns the value according to the criterias price"""

        estimated_value = self.CONST_AVERAGE
        if (storeitem.price):
            # Having a higher price reduces the value
            estimated_value -= self.CONST_SPREAD_FACTOR *self.__price_weight *(storeitem.price - self.__price['average']) / math.sqrt(
                self.__price['variance'])


        if (storeitem.created_on):
            # Higher time since posted reduces the value
            date_time_value = int(storeitem.created_on.strftime('%m%d%H'))
            time_since_posted = self.CURRENT_TIME - date_time_value
            estimated_value -= self.CONST_SPREAD_FACTOR *self.__recency_weight* (time_since_posted - self.__recency['average']) / math.sqrt(
                self.__recency['variance'])

        if (storeitem.popularity):
            # Having a high popularity  increases the value
            estimated_value += self.CONST_SPREAD_FACTOR * self.__popularity_weight*(
                        storeitem.popularity - self.__popularity['average']) / math.sqrt(
                self.__popularity['variance'])

        return int(estimated_value)

    def quick_sort(self, list, startindex, endindex):
        """Recursive function to separate partitions to sort"""

        initial_pivot_value = self.get_initial_pivot(list, startindex, endindex)

        self.quick_sort_helper(list, startindex, endindex, initial_pivot_value)

    def quick_sort_helper(self, list, startindex, endindex, pivotvalue):
        """Recursive function to separate partitions to sort"""
        if startindex < endindex:
            new_center_index = self.partition(list, startindex, endindex, pivotvalue)

            # item a center index is now at the right partition
            left_pivot = self.get_set_pivot(list, startindex, new_center_index - 1)
            self.quick_sort_helper(list, startindex, new_center_index - 1, left_pivot)

            if (new_center_index + 1) <= endindex:
                right_pivot = self.get_set_pivot(list, new_center_index + 1, endindex)
                self.quick_sort_helper(list, new_center_index + 1, endindex, right_pivot)

    def partition(self, list, startindex, endindex, pivotvalue):
        """Handles putting the pivot at right position and distribute smaller then pivot to the left
        and bigger element to the right
        """
        border_index = startindex + 1

        for i in range(border_index, endindex + 1):

            if list[i]['estimated_value'] >= pivotvalue:
                list[i], list[border_index] = list[border_index], list[i]

                border_index += 1

        pivot_index = border_index - 1
        list[startindex], list[pivot_index] = list[pivot_index], list[startindex]
        return pivot_index

    def get_set_pivot(self, list, startindex, endindex):
        """
        Returns the median of 3 values  start, middle and end of the list
        Sets the pivot at startindex position of the list
        """
        # TODO Refactor
        if (endindex - startindex) > 2:
            middle_index = int((startindex + endindex) / 2)
            if ((list[startindex]['estimated_value'] <= list[middle_index]['estimated_value']) &
                    (list[middle_index]['estimated_value'] <= list[endindex]['estimated_value']) | (
                            list[endindex]['estimated_value'] <= list[middle_index]['estimated_value']) &
                    (list[middle_index]['estimated_value'] <= list[startindex]['estimated_value'])):
                list[startindex], list[middle_index] = list[middle_index], list[startindex]
                return list[startindex]['estimated_value']
            if ((list[middle_index]['estimated_value'] <= list[startindex]['estimated_value']) &
                    (list[startindex]['estimated_value'] <= list[endindex]['estimated_value']) | (
                            list[endindex]['estimated_value'] <= list[startindex]['estimated_value']) &
                    (list[startindex]['estimated_value'] <= list[middle_index]['estimated_value'])):
                return list[startindex]['estimated_value']
            else:
                list[startindex], list[endindex] = list[endindex], list[startindex]
                return list[startindex]['estimated_value']

        else:

            return list[startindex]['estimated_value']

    def get_initial_pivot(self, list, startindex, endindex):
        """Returns the value closest to the const average"""
        if (endindex - startindex) > 2:
            middle_index = int((startindex + endindex) / 2)
            start_difference = abs(self.CONST_AVERAGE - list[startindex]['estimated_value'])

            middle_difference = abs(self.CONST_AVERAGE - list[middle_index]['estimated_value'])
            end_difference = abs(self.CONST_AVERAGE - list[endindex]['estimated_value'])
            if end_difference <= middle_difference & end_difference <= start_difference:
                list[startindex], list[endindex] = list[endindex], list[startindex]

            if middle_difference <= start_difference & middle_difference <= end_difference:
                list[startindex], list[middle_index] = list[middle_index], list[startindex]

        return list[startindex]['estimated_value']
