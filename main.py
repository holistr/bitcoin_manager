import requests
import time
from datetime import datetime

# переменные, которые содержат url-адрес цены XRP
base = 'https://fapi.binance.com'
path = '/fapi/v1/ticker/price'
url = base + path

# отправитель уведомлений
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{your-IFTTT-key}'


# функция выводит последнее значение xrp
def get_latest_xrp_price():
    param = {'symbol': 'XRPUSDT'}
    response = requests.get(url, params=param)
    response_json = response.json()
    if response.status_code == 200:
        print(f'Последняя цена XRP:', response_json['price'])
    else:
        print('error')
    return response_json['price']


# выдает последние значения в таблицу
def format_xrp_history(xrp_history):
    rows = []
    for xrp_price in xrp_history:
        date = xrp_price['date'].strftime('%d.%m.%Y %H:%M')
        price = xrp_price['price']
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    return '<br>'.join(rows)


# веб-перехватчик с ценой
def post_ifttt_webhook(event, value):
    data = {'value1': value}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    requests.post(ifttt_event_url, json=data)


# позволяет работать в текущем режиме, пока цена не упадет на 1%
def main():
    xrp_history = []
    while True:
        price = get_latest_xrp_price()
        date = datetime.now()
        xrp_history.append({'date': date, 'price': price})

        smallest_price = 0.99 * float(price)
        if float(price) < smallest_price:
            print(f'Цена упала на 1% и составляет {smallest_price}')

        # Как только у нас будет 5 элементов в нашей xrp_history, отправьте обновление
        if len(xrp_history) == 5:
            post_ifttt_webhook('xrp_price_update', format_xrp_history(xrp_history))
            # сбросить историю
            xrp_history = []
        # ничего не делать одну минуту
        time.sleep(1 * 60)


if __name__ == '__main__':
    main()
