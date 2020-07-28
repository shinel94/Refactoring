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
        volumeCredits = 0
        volumeCredits += max(aPerformance["audience"] - 30, 0)
        if playFor(aPerformance)["type"] == "comedy":
            volumeCredits += aPerformance["audience"] // 5
        return volumeCredits

    totalAmount = 0
    volumeCredits = 0
    result = f'청구 내역 (고객 명 : {invoice["customer"]})\n'
    num2usd = lambda cent_value: f"${cent_value/100:,.2f}"
    for perf in invoice["performances"]:
        volumeCredits += volumeCreditsFor(perf)
        result += f' {playFor(perf)["name"]} : {num2usd(amountFor(perf))} ({perf["audience"]}석)\n'
        totalAmount += amountFor(perf)
    result += f'총액: {num2usd(totalAmount)}\n'
    result += f'적립 포인트: {volumeCredits}점\n'
    return result


def main():
    invoice = json.load(open('./data/invoices.json'))
    plays = json.load(open('./data/plays.json'))
    return statement(invoice, plays)


if __name__ == '__main__':
    print(main())