import requests
import datetime 
import json
import time


headers = { 
        'user-agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0', 
        'accept' :'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'upgrade-Insecure-Requests' : '1',
        'accept-Language' : 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'cache-Control' : 'no-cache'
        }

url = 'https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-product-by-symbol?symbol=XRPUSDT'


def sync_funck(url, headers):
    session = requests.Session()   # Открываем сессию
    max_price = {'price': 0, 'time': None}
    interval = datetime.timedelta(hours=1, minutes=0, seconds=0)
    while True:
        response = session.get(url, headers=headers)   # Делаем запрос
        price = float(json.loads(response.text)['data']['c'])   # Достаем цену

        print(price)

        if price > max_price['price']:  
            max_price['price'] = price  
            max_price['time'] = time.strftime('%T')   # текущее время устанавливаем новой максимальной цене
            print('максимальная цена' , max_price['price'], max_price['time'])

        if '{:.10f}'.format(max_price['price'] - price) == '{:.10f}'.format(max_price['price'] / 100 * 1) and\
            datetime.datetime.strptime(time.strftime('%T'),'%H:%M:%S')- datetime.datetime.strptime(max_price['time'],'%H:%M:%S') <= interval:
            # сравниваем разницу максимальной и минемальной цены с одним процентом от максимальной
            # сравниваем разницу между нынешним временем и временем получения максимальной цены не более часа
            print('Упало на 1%')
            max_price['price'] = price   # ставим нынешнюю цену максимальной
            max_price['time'] = time.strftime('%T') # обновляем время на нынешнее
        time.sleep(0.3) # задержка что-бы не блокнули 

 
if __name__ == '__main__':
    sync_funck(url, headers)
