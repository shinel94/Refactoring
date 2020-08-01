from util.CONSTANT import PASS

class Tester():

    def __init__(self):
        pass

    def value_test(self, return_value, correct_value):
        if return_value == correct_value:
            return PASS
        else:
            raise ValueError(f'Returned Value : {return_value}\n'
                             f'Correct Value : {correct_value}')