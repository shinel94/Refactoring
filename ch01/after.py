import json


def amountFor(aPerformance, play):
    result = 0
    if play["type"] == 'tragedy':
        result = 40000
        if aPerformance["audience"] > 30:
            result += 1000 * (aPerformance["audience"] - 30)
    elif play["type"] == 'comedy':
        result = 30000
        if aPerformance["audience"] > 20:
            result += 10000 + 500 * (aPerformance["audience"] - 20)
        result += 300 * aPerformance["audience"]
    else:
        raise ValueError(f'알 수 없는 장르: {play["type"]}')
    return result

def statement(invoice, plays):
    totalAmount = 0
    volumeCredicts = 0
    result = f'청구 내역 (고객 명 : {invoice["customer"]})\n'
    format_ = lambda cent_value: f"${cent_value:,.2f}"
    for perf in invoice["performances"]:
        play = plays[perf["playID"]]

        thisAmount = amountFor(perf, play)

        volumeCredicts += max(perf["audience"] - 30, 0)
        if play["type"] == "comedy":
            volumeCredicts += perf["audience"] // 5
        result += f' {play["name"]} : {format_(thisAmount/100)} ({perf["audience"]}석)\n'
        totalAmount += thisAmount
    result += f'총액: {format_(totalAmount/100)}\n'
    result += f'적립 포인트: {volumeCredicts}점\n'
    return result


def main():
    invoice = json.load(open('./data/invoices.json'))
    plays = json.load(open('./data/plays.json'))
    return statement(invoice, plays)


if __name__ == '__main__':
    print(main())