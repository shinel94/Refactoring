def sampleProvinceData():
    return {'name': 'Asia',
            'producers': [
                {'name': 'Byzantium', 'cost': 10, 'production': 9},
                {'name': 'Attalia', 'cost': 12, 'production': 10},
                {'name': 'Sinope', 'cost': 10, 'production': 6},
            ],
            'demand': 30,
            'price': 20}


if __name__ == '__main__':
    from ch04.Province import Province
    from ch04.Producer import Producer
    asia = Province(sampleProvinceData())
    from util.Tester import Tester
    from util.CONSTANT import PASS
    tester = Tester()
    signal = tester.value_test(asia.shortfall(), 5)
    if signal == PASS:
        print('pass')
    signal = tester.value_test(asia.profit(), 230)
    if signal == PASS:
        print('pass')

    asia._producers[0]['production'] = 20
    asia.update_totalProduction()
    if tester.value_test(asia.shortfall(), -6) == PASS:
        print('pass')

    if tester.value_test(asia.profit(), 292) == PASS:
        print('pass')
