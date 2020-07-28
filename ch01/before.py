import json

def statement(invoice, plays):
    totalAmount = 0
    volumeCredicts = 0
    result = f'청구 내역 (고객 명 : {invoice["customer"]})\n'
    format_ = lambda cent_value: f"${cent_value:,.2f}"
    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        thisAmount = 0
        if play["type"] == 'tragedy':
            thisAmount = 40000
            if perf["audience"] > 30:
                thisAmount += 1000 * (perf["audience"] - 30)
        elif play["type"] == 'comedy':
            thisAmount = 30000
            if perf["audience"] > 20:
                thisAmount += 10000 + 500*(perf["audience"] - 20)
            thisAmount += 300 * perf["audience"]
        elif play["type"] == 'crime':
            thisAmount = 50000
            if perf["audience"] > 30:
                thisAmount += 25000 + 1000*(perf["audience"] - 30)
            thisAmount += 500 * perf["audience"]
        else:
            raise ValueError(f'알 수 없는 장르: {play["type"]}')
        volumeCredicts += max(perf["audience"] - 30, 0)
        if play["type"] == "comedy":
            volumeCredicts += perf["audience"] // 5
        elif play["type"] == 'crime':
            volumeCredicts += perf["audience"] // 3
        result += f' {play["name"]} : {format_(thisAmount/100)} ({perf["audience"]}석)\n'
        totalAmount += thisAmount
    result += f'총액: {format_(totalAmount/100)}\n'
    result += f'적립 포인트: {volumeCredicts}점\n'
    return result


def main(invoice_path, plays_path):
    invoice = json.load(open(invoice_path))
    plays = json.load(open(plays_path))
    return statement(invoice, plays)


if __name__ == '__main__':
    print(main())