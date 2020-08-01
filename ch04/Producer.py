from ch04.Province import Province

class Producer:
    def __init__(self, aProvince: Province, data):
        self._province = aProvince
        self._cost = data['cost']
        self._name = data['name']
        self.set_production(data['production'])

    def set_production(self, production):
        try:
            self._production = int(production)
        except ValueError:
            self._production = 0 # data['production']이 int가 아닌 경우 0으로 할당

        self._province._totalProduction += self._production - self._production