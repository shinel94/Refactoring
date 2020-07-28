from abc import *

def createStatementData(invoice, plays):
    statementData = {}

    def playFor(aPerformance):
        return plays[aPerformance["playID"]]

    def totalVolumeCredits(data):
        return sum([x["volumeCredits"] for x in data["performances"]])

    def totalAmount(data):
        return sum([x["amount"] for x in data["performances"]])

    statementData["customer"] = invoice["customer"]
    statementData["performances"] = invoice["performances"]
    [x.update({"play" : createPerformanceCalculator(x, playFor(x)).play, "amount": createPerformanceCalculator(x, playFor(x)).amountFor(), "volumeCredits": createPerformanceCalculator(x, playFor(x)).volumeCreditsFor()}) for x in statementData["performances"]] # update에 적절한 코드를 알고 있지 못해서 추후 개선 필요
    statementData["totalAmount"] = totalAmount(statementData)
    statementData["totalVolumeCredits"] = totalVolumeCredits(statementData)
    return statementData

def createPerformanceCalculator(aPerformance, aPlay):
    if aPlay["type"] == 'tragedy':
        return TragedyCalculator(aPerformance, aPlay)
    elif aPlay["type"] == "comedy":
        return ComedyCalculator(aPerformance, aPlay)


class PerformanceCalculator:

    def __init__(self, aPerformance, aPlay):
        self.performance = aPerformance
        self.play = aPlay

    @abstractmethod
    def amountFor(self):
        raise NotImplementedError(f'알 수 없는 장르: {self.play["type"]}')

    def volumeCreditsFor(self):
        result = 0
        result += max(self.performance["audience"] - 30, 0)
        return result

class TragedyCalculator(PerformanceCalculator):

    def amountFor(self):
        result = 40000
        if self.performance["audience"] > 30:
            result += 1000 * (self.performance["audience"] - 30)
        return result

class ComedyCalculator(PerformanceCalculator):

    def amountFor(self):
        result = 30000
        if self.performance["audience"] > 20:
            result += 10000 + 500 * (self.performance["audience"] - 20)
        result += 300 * self.performance["audience"]
        return result

    def volumeCreditsFor(self):
        return super(ComedyCalculator, self).volumeCreditsFor() + self.performance["audience"] // 5

    