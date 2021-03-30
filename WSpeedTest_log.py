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
        print('\tInternet connection is down: {}\n'.format(t))


def wr_dwnup():  # Записваем результат в читабильный вид в file.txt, второй файл можно использовать для построения аналитики и графиков
    if connect():
        d, u, p, t, i, comp = get_dwnup()
        print('Testing: {}\n'.format(t))
        print('\tDownload: {} Mb/s\n'.format(d))
        print('\tUpload: {} Mb/s\n'.format(u))
        # дописываем в файлы, а не перезаписываем
        with open('file.csv', 'a') as f:
            f.write('{},{},{},{},{},{}\n'.format(d, u, p, t, i, comp))
        with open('file.txt', 'a') as f:
            f.write('Test start :{}\n'.format(t))
            f.write('\tIp address: {}\n'.format(i))
            f.write('\tProvider: {}\n'.format(comp))
            f.write('\tDownload: {} Mb/s\n'.format(d))
            f.write('\tUpload: {} Mb/s\n'.format(u))
            f.write('\tPing: {}\n'.format(p))
        try:
            messg = 'ip: ' + str(i) + ' Dwn: ' + str(d) + 'Mb/s Up: ' + str(u) + 'Mb/s ping: ' + str(p)
            requests.get('https://api.telegram.org/bot< API TELEGRAM >/sendMessage?chat_id=< CHAT_ID >&text=' + messg)
        except:
            with open('file.txt', 'a') as f:
                f.write('\tapi.Telegram id Down!\n')
    else:
        t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('file.txt', 'a') as f:
            f.write('Test start :{}\n'.format(t))
            f.write('\tInternet connection is down: {}\n'.format(t))


# аргумент используемый для завершения и запуска работы задач и скрипта
globvar = 1
with open('file.csv', 'w') as f:
    f.write('download,upload,ping,time,ip,tProvider\n')
with open('file.txt', 'w') as f:
    f.write('Let\'s start \n')

# настриваем наши планировщики

schedule.every(15).minutes.do(wr_dwnup).tag('tasks')  # основная функция

while globvar == 1:
    # запускаем наши планировщики
    schedule.run_pending()
    time.sleep(1)
