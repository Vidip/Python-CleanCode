import requests
import json
import abc
import argparse
import sys
from fuzzywuzzy import fuzz

CALORIE_RANGE = {
    'pizza': 200,
    'burger': 500,
    'chips': 100,
    'grilled chicken': 600
}

FOOD_LIST = ['pizza', 'burger', 'chips', 'grilled chicken']

class CalorieCounter:

    def __init__(self, food):
        self.__food = food

    def calculate_counter(self):
        if self.__food in CALORIE_RANGE:
            return CALORIE_RANGE[self.__food]


class CafeReviews(metaclass=abc.ABCMeta):

   @abc.abstractmethod
   def read_cafe_reviews(self):
      pass

"""
Methods and API call within a Class will help to scale large
production grade APIs, allowing us to implement Abstract Classes and
follwing the Abstraction in larger production grade applications
"""

class GetCafeLocation(CafeReviews, CalorieCounter):
    def __init__(self, food, url=''):
        """
        made api url as protected variable to notify users that this
        variable is protected and needs not to be changed
        """
        self.food = food
        if url:
            self._api_url = url
        else:
            self._api_url = "http://localhost:3306/desserts"

    @classmethod
    def get_list_of_favourite_food(cls):
        return FOOD_LIST

    def __call__(self):
        """
        Using call method will help to hide method functions or avoid direct
        method call, thus a object can be used as a function to get
        the response
        """
        self.read_api_data()

    def do_api_call(self):
        response = ''
        try:
            response = requests.get(self._api_url)
        except Exception as e:
            # Raising Excpetion
            raise Exception("API Call Failed: {}".format(e)) from None
        return response

    def read_api_data(self):
        response = self.do_api_call()
        if response.status_code == 200:
            """
            try except block to handle the errors that can be raised
            while Json loads
            """
            try:
                highest_score = -1
                final_cafe_name = ''
                data = json.loads(response.text)
                for _ in data:
                    fuzz_value = fuzz.ratio(_.get('famous'), self.food)
                    if fuzz_value > highest_score:
                        highest_score = fuzz_value
                        final_cafe_name = _.get('name')
                """ print
                statements, logging or return from a function can be used
                """
                print('Your favourite food can be found at cafe - {}'.format(final_cafe_name))\
                if highest_score > 0 else print("No Cafe Found")

                if highest_score > 0:
                    self.read_cafe_reviews()
                    super().__init__(self.food)
            except Exception as e:
                # Rasing Exception if Json Loads Fails
                raise Exception("Data Load Failed: {}".format(e)) from None
        else:
            print('Request was unsuccessful: {}'.format(response.status_code))


    def read_data(self, file_object, chunk_size=100):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 100 bytes."""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data


    def read_cafe_reviews(self):
        with open('big_file.txt') as f:
            for chunk in self.read_data(f):
                pass
            f.close()


if __name__ == "__main__":
    print(GetCafeLocation.get_list_of_favourite_food())
    parser = argparse.ArgumentParser()
    parser.add_argument("food_item", metavar='food_item', help="please tell what food you want to eat",
                type=str)
    args = parser.parse_args()
    if args:
        get_cafe_location = GetCafeLocation(args.food_item.split('food_item=')[1])
        get_cafe_location()
        print("Calorie of {} is {}".format(args.food_item.split('food_item=')[1], get_cafe_location.calculate_counter()))
