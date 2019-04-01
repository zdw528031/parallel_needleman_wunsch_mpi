import unittest
import random
#random.randint(1,101)

def max_vaule_of_three_and_find_where_it_come_from(vertical,horizontal,diagonal):
    if diagonal < horizontal and diagonal < vertical:
        if horizontal == vertical:
            return horizontal,3
        if vertical > horizontal:
            return vertical,1
        return horizontal,2
    else:
        if diagonal > horizontal and diagonal > vertical:
            return diagonal,4 #ONLY_DIAGONAL
        if vertical > horizontal:
            if vertical == diagonal:
                return vertical,5
            return vertical,1
        if horizontal > vertical:
            if horizontal == diagonal:
                return horizontal,6
            return horizontal,2
        return diagonal,7


class TestStringMethods(unittest.TestCase):

    def test_ramdon_input_(self):
        for i in range(1000000):
            vertical_value = random.randint(1,16) #random number between 1~15
            horizontal_value = random.randint(1,16) #random number between 1~15
            diagonal_value = random.randint(1,16) #random number between 1~15
            return_value = max_vaule_of_three_and_find_where_it_come_from(vertical_value,horizontal_value,diagonal_value)
            max_value = max(vertical_value,max(horizontal_value,diagonal_value))
            self.assertEqual(return_value[0],max_value)
            if max_value == vertical_value:
                self.assertEqual(return_value[1]%2,1)
            if max_value == horizontal_value:
                self.assertNotEqual(return_value[1],1)
                self.assertNotEqual(return_value[1],4)
                self.assertNotEqual(return_value[1],5)
            if max_value == diagonal_value:
                self.assertGreaterEqual(return_value[1],4)

if __name__ == '__main__':
    unittest.main()