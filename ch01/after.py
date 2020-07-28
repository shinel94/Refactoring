import json


def statement(invoice, plays):

    def playFor(aPerformance):
        return plays[aPerformance["playID"]]

    def amountFor(aPerformance):
        result = 0
        if playFor(aPerformance)["type"] == 'tragedy':
            result = 40000
            if aPerformance["audience"] > 30:
                result += 1000 * (aPerformance["audience"] - 30)
        elif playFor(aPerformance)["type"] == 'comedy':
            result = 30000
            if aPerformance["audience"] > 20:
                result += 10000 + 500 * (aPerformance["audience"] - 20)
            result += 300 * aPerformance["audience"]
        else:
            raise ValueError(f'알 수 없는 장르: {playFor(aPerformance)["type"]}')
        return result

    def volumeCreditsFor(aPerformance):
        result = 0
        result += max(aPerformance["audience"] - 30, 0)
        if playFor(aPerformance)["type"] == "comedy":
            result += aPerformance["audience"] // 5
        return result

    def totalVolumeCredits():
        result = 0
        for perf in invoice["performances"]:
            result += volumeCreditsFor(perf)
        return result

    def totalAmount():
        result = 0
        for perf in invoice["performances"]:
            result += amountFor(perf)
        return result

    num2usd = lambda cent_value: f"${cent_value/100:,.2f}"

    ##### main statement code #####
    result = f'청구 내역 (고객 명 : {invoice["customer"]})\n'

    for perf in invoice["performances"]:
        result += f' {playFor(perf)["name"]} : {num2usd(amountFor(perf))} ({perf["audience"]}석)\n'

    result += f'총액: {num2usd(totalAmount())}\n'
    result += f'적립 포인트: {totalVolumeCredits()}점\n'
    
    return result


def main():
    invoice = json.load(open('./data/invoices.json'))
    plays = json.load(open('./data/plays.json'))
    return statement(invoice, plays)


if __name__ == '__main__':
    print(main())