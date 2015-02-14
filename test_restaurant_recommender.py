import unittest
from restaurant_recommender import RestaurantRecommender

# This module contains the test cases for module restaurant_recommender.


class TestRestaurantRecommender(unittest.TestCase):
    def setUp(self):
        self.recommender1 = RestaurantRecommender("sample_data.csv")
        self.recommender2 = RestaurantRecommender("sample_data_2.csv")

    def test_menu_item_not_found(self):
        result = self.recommender1.recommend(['tea', 'paneer'])
        self.assertEqual(result, "Nil")
  
    def test_number_of_restaurants(self):
        self.assertEqual(len(self.recommender1.restaurant_items.keys()), 6)
        self.assertEqual(len(self.recommender2.restaurant_items.keys()), 2)
  
    def test_best_price_restaurant(self):
        result = self.recommender1.recommend(['tofu_log', 'burger'])
        result = result.split(" ")
        self.assertEqual('2', result[0])
        self.assertEqual('11.5', result[1])
        result = self.recommender1.recommend(['chef_salad', 'wine_spritzer'])
        self.assertEqual('Nil', result)
        result = self.recommender1.recommend(['extreme_fajita',
                                              'fancy_european_water'])
        result = result.split(" ")
        self.assertEqual('6', result[0])
        self.assertEqual('11.0', result[1])

        result = self.recommender2.recommend(['tea', 'coffee'])
        result = result.split(" ")
        self.assertEqual('1', result[0])
        self.assertEqual('5.0', result[1])

        
     
if __name__ == "__main__":
    unittest.main()
