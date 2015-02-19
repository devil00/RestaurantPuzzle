'''
This module is the solution of Jurgensville Restaurant puzzle.
@author: Mayur Swami
@Date: 19-Feb-2015
'''
import os
import csv
import sys
from collections import defaultdict
from itertools import combinations

from errors import FileReadError


PRICE_MAX_CONST = 1000000000000.00


class RestaurantRecommender(object):
    def __init__(self, restaurant_file):
        self.restaurant_file = restaurant_file
        self._check_file_validity()
        self.restaurant_items = self._prepare_restaurant_menu()

    def _check_file_validity(self):
        '''
        Check th validity of a csv file feeded as an input.
        '''
        file_validity = (
            os.path.exists(self.restaurant_file) and 
            os.path.getsize(self.restaurant_file) > 0 and 
            os.path.splitext(self.restaurant_file)[1] == ".csv")
        if not file_validity:
            raise FileReadError("Invalid input file.")

    def _prepare_restaurant_menu(self):
        '''
        It will prepare a restaurants map with all the available items. If
        mutiple entries are found then the item with minimum price will be 
        selected.
        '''
        # Map of resturant id to price list of items. e.g.,
        # {'1': {'item': 'burger', 'price': 12.4},
        # {'item': ['burger, pizza'], 'price': 34.2}], ..}
        rest_items = defaultdict(list)
        with open(self.restaurant_file, "rb") as f:
            seen_rows = set()
            reader = csv.reader(f)
            for row in reader:
                # Only consider unique row.
                try:
                    restaurant_id = int(row[0].strip())
                    price = float(row[1].strip())
                    item = tuple([r.strip().lower() for r in sorted(row[2:])])
                except IndexError:
                    continue
                item_row = (restaurant_id, price, item,)
                if not self.validate(restaurant_id, price, item):
                    print "Escaping Invalid rows : {}".format(item_row)
                    continue
                if item_row in seen_rows:
                    continue
                seen_rows.add(item_row)
                rest_items[restaurant_id].append(
                    {
                        'price': price,
                        'item': item
                    }
                )
        return rest_items

    def validate(self, rid, price, item_list):
        return (rid > 0 and price > 0.0 and item_list is not None)

    def _prepare_order_item_hash_from_restaurant_menu(self, order_items,
                                                      restaurant_items):
        order_hash = defaultdict(list)
        for item in order_items:
            for rest_item in restaurant_items:
                if item in rest_item['item']:
                    order_hash[item].append(rest_item)
            # If any of the order_item is not available in a resturant menu,
            # then immediately get out of the iteration.
            if not order_hash:
                break
        return order_hash

    def _compute_minimum_price_for_order(self, menu_order_hash, order_items):
        if len(order_items) == 0 or not order_items:
            return 0.0
        item_to_satisfy = order_items[0]
        menus = menu_order_hash[item_to_satisfy]
        current_min_price = PRICE_MAX_CONST
        for menu_item in menus:
            mprice = self._compute_minimum_price_for_order(
                menu_order_hash, [item for item in order_items \
                                  if item not in menu_item['item']])
            possible_min_price = menu_item['price'] + mprice
            if possible_min_price < current_min_price:
                current_min_price = possible_min_price
        return current_min_price


    def recommend(self, menu_items):
        '''
        It will select all the restaurant where menu is available and
        return the one with the minimum price for this menu.
        :param menu_items: Menu provided by user.
        :type menu_items: list
        '''
 
        selected_restaurants = {}
        menu_items = [item.strip().lower() for item in menu_items]
        for restaurant_id, items_info in self.restaurant_items.items():
            order_items = menu_items[:]
            menu_order_hash = \
                    self._prepare_order_item_hash_from_restaurant_menu(
                        order_items, items_info)
            if not menu_order_hash:
                continue
            if len(set(menu_order_hash.keys()).intersection(
                order_items)) == len(order_items):
                min_price = self._compute_minimum_price_for_order(
                    menu_order_hash, order_items)

                selected_restaurants[restaurant_id] = min_price
        if not selected_restaurants:
            return "Nil"
        else:
            result = min(selected_restaurants.items(), key=lambda l: l[1])
            return "{} {}".format(result[0], result[1])


def main():
    if len(sys.argv) < 3:
        print 'Nil'
        return

    restaurant_items_file = sys.argv[1]
    menu_items = list(set(sys.argv[2:]))
    rr = RestaurantRecommender(restaurant_items_file)
    print rr.recommend(menu_items)


if __name__ == "__main__":
    main()
