import math
from datetime import datetime


class ItemSortManager:

    def __init__(self, storeitems, priceweight, recencyweight, popularityweight):
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
        current_date = int(datetime.now().strftime('%m%d%H'))

        for storeitem in storeitems:
            if storeitem.price:
                sum['price'] += storeitem.price
                variance_sum['price'] += math.pow(storeitem.price, 2)
            if storeitem.popularity:
                sum['popularity'] += storeitem.popularity
                variance_sum['popularity'] += math.pow(storeitem.popularity, 2)
            if storeitem.created_on:
                date_time_value = int(storeitem.created_on.strftime('%m%d%H'))
                time_since_posted = current_date - date_time_value
                sum['recency'] += time_since_posted
                variance_sum['recency'] += math.pow(time_since_posted, 2)

        self.__price = {
            'average': sum['price'] / items_quantity,
            'variance': variance_sum['price'] / (items_quantity - 1)
        }
        self.__popularity = {
            'average': sum['popularity'] / items_quantity,
            'variance': variance_sum['popularity'] / (items_quantity - 1)
        }
        self.__recency = {
            'average': sum['recency'] / items_quantity,
            'variance': variance_sum['recency'] / (items_quantity - 1)
        }

        print(self.__price['average'])

    def get_estimated_value(self, storeitem):
        """Returns the value according to the """
