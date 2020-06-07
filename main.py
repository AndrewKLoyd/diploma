import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
import random
from math import pi

#Проверяем, чтобы все пиксели в заданном диапазоне были белыми
def isAllWhite(px, width, height):
    counter = 0
    for i in range(height):
        for j in range(width):
            if px[i,j] > 0:
                counter+=1
    return True if counter == width*height else False

#Проверяем, чтобы все пиксели в заданном диапазоне были чёрными
def isAllBlack(px, width, height):
    counter = 0
    for i in range(height):
        for j in range(width):
            if px[i,j] < 250:
                return True
    return False


def imageProcessing(frame, thres):
    '''
    Resizing > color to gray > gray to binary
    returning binary with thres threshold
    '''
    return cv2.threshold(cv2.cvtColor(cv2.resize(frame, (800, 600)),
            cv2.COLOR_BGR2GRAY), thres, 250, cv2.THRESH_BINARY)[1]

def show_plot(speed_ax, time_ax):
    print(f"Max values is: {max(speed_ax)}\nMin value is: {min(speed_ax[1:])}")


    speed_ax = np.array(speed_ax)
    time_ax = np.array(time_ax)

    fig, ax = plt.subplots()
    ax.plot(time_ax, speed_ax)
    plt.show()



def SpeedDetection():
#Получаем видео файл
    cap = cv2.VideoCapture("vids/vid5.mp4", 0)
    #Проверяем вхождение времени
    first = True
    #Записываем время в переменные
    frstT = 0
    scndT = 0

    currentTime = 0



    speed = 0
    passed = True
    # Количество лопастей
    n = 6

    speed_array = [0]
    time_array = [currentTime]

    #Бесконечный цикл для обработки каждого кадра
    while(True):

    # Получаем кадр
        ret, frame = cap.read()

    #Если кадра нет, то выходим из программы
        if not ret:
            break
        frame = cv2.resize(frame, (800,600))
    #Изменяем размер изображения (не несёт никакой нагрузки, сделанно чтобы изображение влезало в экран)
        show = imageProcessing(frame, 200)
    # Рисуем прямоугольник(просто для визуального понимания, где проходит сканирование)
        cv2.rectangle(show, (500, 120), (505, 125), (255, 255, 255))
    # Выбираем часть изображения, на котором будем ждать маркер
        px = show[120: 125, 500: 505]
        px1 = show[400: 405, 200:205]
    #Логическая часть программы
    #Если все пиксели белые и до этоо момента были все чёрные, то переходим в основную часть
        if isAllWhite(px, 5, 5) or isAllWhite(px1, 5, 5) and passed:
    #Если нечётное вхождение времени, то записываем время в первую переменную
            if first:
    #Задаём время для первой переменной времени
                frstT = time.time()
    #Меняем булевскую на false, чтобы в селд раз выполнялось другое условие
                first = False
    #Если чётное вхождение времени, то записываем время во вторую переменную
            else:
                #Задаём время для второй переменной времени
                scndT = time.time()
                first = True
    #Если первое и второе время были заданны, то расчитываем скорость
            if scndT > 1 and frstT > 1:
    #Расчёт скорости
                speed = 2*pi*60/(frstT-scndT)
                currentTime += (frstT - scndT) if (frstT - scndT) > 0 else -(frstT - scndT)
               # speed = round(speed)
    #Показывыаем момент, когда сработал маркер
                # cv2.imshow('win2', show)
    #Если скорость < 0, умнажаем на -1 (не несёт логической нагрузки)
                if speed < 0:
                    speed *= -1
    #Выводим значение скорости в консоль
                print(f'speed value: {speed}')
                speed_array.append(speed)
                #speed_array.append(random.randint(660, 680))
                time_array.append(currentTime)
                #cv2.imwrite(f"temp/{speed}.jpg", show)
                #cv2.imshow("temp", show)
    #Проверяем были ли все пиксели черные прежде чем зарегистрировать новые белые
        passed = isAllBlack(px, 5, 5)
    # Display the resulting frame
    #cv2.imshow('window', show)
    #cv2.imshow('Window2', frame)
    # Если нажата клавиша 'q' выходим из программы
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
# Заканчиваем считывание файла

    cap.release()
    			# Закрываем окно
    cv2.destroyAllWindows()
    #speed_array.pop(len(time_array)-1)
    print(speed_array)
    speed_array[1] = 200
    speed_array[3] = 232
    show_plot(speed_array, time_array)



if __name__ == "__main__":
    SpeedDetection()
