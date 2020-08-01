class Province:
    def __init__(self, doc_json):
        self._name = doc_json['name']
        self._producers = []
        self._totalProduction = 0
        self._demand = doc_json['demand']
        self._price = doc_json['price']
        for producer in doc_json['producers']:
            self.add_producer(producer)

    def add_producer(self, producer):
        self._producers.append(producer)
        self._totalProduction += producer['production']

    def update_totalProduction(self):
        self._totalProduction = 0
        for producer in self._producers:
            self._totalProduction += producer['production']
    # python은 따로 getter와 setter를 추가로 정의하지 않는다.

    def shortfall(self):
        return self._demand - self._totalProduction

    def profit(self):
        return self.demand_value() - self.demand_cost()

    def demand_value(self):
        return self.satisfied_demand() * self._price

    def satisfied_demand(self):
        return min(self._demand, self._totalProduction)

    def demand_cost(self):
        remaining_demand = self._demand
        result = 0
        producer_list = sorted(self._producers, key=lambda x: x['cost'])
        for producer in producer_list:
            contribution = min(remaining_demand, producer['production'])
            remaining_demand -= contribution
            result += contribution*producer['cost']

        return result