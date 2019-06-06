import random
from datetime import datetime

from . import models


class FakeData:

    price_weight=35
    popularity_weight=35
    recency_weight=30


    def get_unordered_item_list(self, item_number):
        unordered_item_list = []
        store_user = models.StoreUserProfile.objects.create()

        for i in range(0, item_number):

            item = models.StoreItem.objects.create(store_user=store_user, item_id=i, item_name="item",
                                                   price=random.randint(0, 100),
                                                   popularity=random.randint(0, 100), created_on=datetime.now())

            unordered_item_list.append(item)

        return unordered_item_list

