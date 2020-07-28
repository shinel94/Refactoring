import json


def statement(invoice, plays):
    return renderPlainText(createStatementData(invoice, plays))

def createStatementData(invoice, plays):
    statementData = {}

    def playFor(aPerformance):
        return {"play": plays[aPerformance["playID"]]}

    def amountFor(aPerformance):
        result = 0
        if aPerformance["play"]["type"] == 'tragedy':
            result = 40000
            if aPerformance["audience"] > 30:
                result += 1000 * (aPerformance["audience"] - 30)
        elif aPerformance["play"]["type"] == 'comedy':
            result = 30000
            if aPerformance["audience"] > 20:
                result += 10000 + 500 * (aPerformance["audience"] - 20)
            result += 300 * aPerformance["audience"]
        else:
            raise ValueError(f'알 수 없는 장르: {aPerformance["play"]["type"]}')
        return {'amount': result}

    def volumeCreditsFor(aPerformance):
        result = 0
        result += max(aPerformance["audience"] - 30, 0)
        if aPerformance["play"]["type"] == "comedy":
            result += aPerformance["audience"] // 5
        return {'volumeCredits': result}

    def totalVolumeCredits(data):
        return sum([x["volumeCredits"] for x in data["performances"]])

    def totalAmount(data):
        return sum([x["amount"] for x in data["performances"]])

    statementData["customer"] = invoice["customer"]
    statementData["performances"] = invoice["performances"]
    [x.update(playFor(x)) for x in statementData["performances"]] # update에 적절한 코드를 알고 있지 못해서 추후 개선 필요
    [x.update(amountFor(x)) for x in statementData["performances"]] # update에 적절한 코드를 알고 있지 못해서 추후 개선 필요
    [x.update(volumeCreditsFor(x)) for x in statementData["performances"]] # update에 적절한 코드를 알고 있지 못해서 추후 개선 필요
    statementData["totalAmount"] = totalAmount(statementData)
    statementData["totalVolumeCredits"] = totalVolumeCredits(statementData)
    return statementData

def num2usd(cent_value):
    return f"${cent_value/100:,.2f}"

def renderPlainText(data):

    ##### main statement code #####
    result = f'청구 내역 (고객 명 : {data["customer"]})\n'

    for perf in data["performances"]:
        result += f' {perf["play"]["name"]} : {num2usd(perf["amount"])} ({perf["audience"]}석)\n'

    result += f'총액: {num2usd(data["totalAmount"])}\n'
    result += f'적립 포인트: {data["totalVolumeCredits"]}점\n'

    return result


def main():
    invoice = json.load(open('./data/invoices.json'))
    plays = json.load(open('./data/plays.json'))
    return statement(invoice, plays)


def htmlStatement(invoice, plays):
    return renderHtml(createStatementData(invoice, plays))

def renderHtml(data):
    result = ''
    result += f'<h1>청구 내역 (고객명: {data["customer"]}</h1>\n'
    result += '<table>\n'
    result += '<tr><th>연극</th><th>좌석 수</th><th>금액</th></tr>'
    for perf in data["performances"]:
        result += f'<tr><td>{perf["play"]["name"]}</td><td>{perf["audience"]}석)</td>'
        result += f'<td>{num2usd(perf["amoun"])}</td></tr>\n'
    result += '</table>\n'
    result += f'<p>총액: <em>${num2usd(data["totalAmount"])}</em></p>\n'
    result += f'<p>적립 포인트: <em>${data["totalVolumeCredits"]}</em>점</p>\n'
    return result

if __name__ == '__main__':
    print(main())