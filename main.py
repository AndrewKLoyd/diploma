import numpy as np
import cv2
import time
import matplotlib.pyplot as plt


#Проверяем, чтобы все пиксели в заданном диапазоне были белыми
def isAllWhite(px, width, height):
    counter = 0
    for i in range(height):
        for j in range(width):
            if px[i,j] > 0:
                counter+=1
    if counter == width*height:
        return True
    else:
        return False

#Проверяем, чтобы все пиксели в заданном диапазоне были чёрными
def isAllBlack(px, width, height):
    global passed
    counter = 0
    for i in range(height):
        for j in range(width):
            if px[i,j] < 250:
                return True
    return False


def imageProcessing(frame):

    frameLoc = cv2.resize(frame, (800, 600), fx=0, fy=0)
                                                                                #В серое изображение
    gray = cv2.cvtColor(frameLoc, cv2.COLOR_BGR2GRAY)
                                                                                # В бинарное изображение
    retval, show = cv2.threshold(gray, 200, 250, cv2.THRESH_BINARY)
    return show




#Получаем видео файл
cap = cv2.VideoCapture("vids/vid5.mp4", 0)

#Проверяем вхождение времени
first = True
#Записываем время в переменные
frstT = 0
scndT = 0




speed = 0
passed = True                    # Количество лопастей
n = 6

fig, ax = plt.subplots()
speed_array = list()
time_array = list()

                                        #Бесконечный цикл для обработки каждого кадра
while(True):

                                            # Получаем кадр
    ret, frame = cap.read()
                                                #Если кадра нет, то выходим из программы
    if not ret:
        break
                                                                    #Изменяем размер изображения (не несёт никакой нагрузки, сделанно чтобы изображение влезало в экран)
    show = imageProcessing(frame)
                                                                    # Рисуем прямоугольник(просто для визуального понимания, где проходит сканирование)
    cv2.rectangle(show, (500, 120), (505, 125), (255, 255, 255))
                                                                                # Выбираем часть изображения, на котором будем ждать маркер
    px = show[120: 125, 500: 505]
                                                                                #Логическая часть программы
                                                                                #Если все пиксели белые и до этоо момента были все чёрные, то переходим в основную часть
    if isAllWhite(px, 5, 5) and passed:
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
            speed = 360/(frstT-scndT)
            speed = round(speed)
            #Показывыаем момент, когда сработал маркер
           # cv2.imshow('win2', show)
            #Если скорость < 0, умнажаем на -1 (не несёт логической нагрузки)
            if speed < 0:
                speed *= -1
            #Выводим значение скорости в консоль
            print(f'speed value: {speed}')
            speed_array.append(speed)
            time_array.append(time.time())
            cv2.imshow("temp", show)
    #Проверяем были ли все пиксели черные прежде чем зарегистрировать новые белые
    passed = isAllBlack(px, 5, 5)

    # Display the resulting frame
    cv2.imshow('window', show)
    cv2.imshow('Window2', frame)
    # Если нажата клавиша 'q' выходим из программы
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Заканчиваем считывание файла
cap.release()
# Закрываем окно
cv2.destroyAllWindows()


#list(map(lambda x: x if int(x)%10==0 else time_array.pop(time_array.index(x)), time_array))
#list(map(lambda x: x if int(x)%10==0 else speed_array.pop(speed_array.index(x)), speed_array))
speed_array = np.array(speed_array)
time_array = np.array(time_array)

print(f"speed {len(speed_array)}: {speed_array} \n time {time_array}: {time_array}")

plt.grid(True)
plt.autoscale(True, axis ="both", tight = True)
ax.plot(time_array, speed_array)
plt.show()
plt.close()
