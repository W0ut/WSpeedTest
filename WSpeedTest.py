# -*- coding: UTF-8 -*-
import speedtest
import schedule
import time
import requests
from datetime import datetime


def connect():
    try:
        URL = 'http://ya.ru'
        r = requests.get(URL)
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def get_dwnup():    # Собираем результат запроса тестирования скорости в переменные
    if connect():
        t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        s = speedtest.Speedtest()
        s.get_servers()
        s.get_best_server()
        s.download()
        s.upload()
        res = s.results.dict()
        # переводим скорость из bytes в Mb
        u = float('{:.2f}'.format(float(res["upload"]) * 0.00000095367432))
        d = float('{:.2f}'.format(float(res["download"]) * 0.00000095367432))
        return d, u, res["ping"], t, res["client"]["ip"], res["client"]["isp"]
    else:
        t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('Internet connection is down {}\n'.format(t))


def wr_dwnup():  # Отправляем результат по telegram
    if connect():
        d, u, p, t, i, comp = get_dwnup()
        print('Testing: {}\n'.format(t))
        print('\tDownload: {} Mb/s\n'.format(d))
        print('\tUpload: {} Mb/s\n'.format(u))
        try:
            messg = 'ip: ' + str(i) + ' Dwn: ' + str(d) + 'Mb/s Up: ' + str(u) + 'Mb/s ping: ' + str(p)
            requests.get('https://api.telegram.org/bot< API TELEGRAM >/sendMessage?chat_id=< CHAT_ID >&text=' + messg)
        except:
            print('\tapi.Telegram id Down! {}\n'.format(t))


# аргумент используемый для завершения и запуска работы задач и скрипта
globvar = 1

schedule.every(10).minutes.do(wr_dwnup).tag('tasks')  # основная функция / настриваем наши планировщики

print('Let\'s start \n')
while globvar == 1:
    # запускаем наши планировщики
    schedule.run_pending()
    time.sleep(1)
