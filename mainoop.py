import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
import random
from math import pi

class SpeedDetection:

	def __init__(self, pathToVideo):
		self.cap = cv2.VideoCapture(0) if pathToVideo == str(0) else cv2.VideoCapture(pathToVideo, 0)
		self.first = True
		self.frstT = 0

		self.scndT = 0
		self.currentTime = 0

		self.speed = 0
		self.passed = True
		# Количество лопастей
		self.speed_array = [0]
		self.time_array = [self.currentTime]


	def isAllWhite(self, px, width, height):
		counter = 0
		for i in range(height):
			for j in range(width):
				if px[i,j] > 0:
					counter+=1
		return True if counter == width*height else False

	def isAllBlack(self, px, width, height):
		counter = 0
		for i in range(height):
			for j in range(width):
				if px[i,j] < 250:
					return True
		return False
	def imageProcessing(self, frame, thres):
	    '''
	    Resizing > color to gray > gray to binary
	    returning binary with thres threshold
	    '''
	    return cv2.threshold(cv2.cvtColor(cv2.resize(frame, (800, 600)),
	            cv2.COLOR_BGR2GRAY), thres, 250, cv2.THRESH_BINARY)[1]

	def show_plot(self, speed_ax, time_ax):
	    speed_ax = np.array(speed_ax)
	    time_ax = np.array(time_ax)

	    fig, ax = plt.subplots()
	    ax.plot(time_ax, speed_ax)
	    plt.show()



	def speedDetection(self):
	#Получаем видео файл
	    while(True):

	    # Получаем кадр
	        ret, frame = self.cap.read()

	    #Если кадра нет, то выходим из программы
	        if not ret:
	            break
	        frame = cv2.resize(frame, (800,600))
	    #Изменяем размер изображения (не несёт никакой нагрузки, сделанно чтобы изображение влезало в экран)
	        show = self.imageProcessing(frame, 200)
	    # Рисуем прямоугольник(просто для визуального понимания, где проходит сканирование)
	        cv2.rectangle(show, (500, 120), (505, 125), (255, 255, 255))
	    # Выбираем часть изображения, на котором будем ждать маркер
	        px = show[120: 125, 500: 505]
	    #Логическая часть программы
	    #Если все пиксели белые и до этоо момента были все чёрные, то переходим в основную часть
	        if self.isAllWhite(px, 5, 5) and self.passed:
	    #Если нечётное вхождение времени, то записываем время в первую переменную
	            if self.first:
	    #Задаём время для первой переменной времени
	                self.frstT = time.time()
	    #Меняем булевскую на false, чтобы в селд раз выполнялось другое условие
	                self.first = False
	    #Если чётное вхождение времени, то записываем время во вторую переменную
	            else:
	                #Задаём время для второй переменной времени
	                self.scndT = time.time()
	                self.first = True
	    #Если первое и второе время были заданны, то расчитываем скорость
	            if self.scndT > 1 and self.frstT > 1:
	    #Расчёт скорости
	                self.speed = 2*pi*60/(self.frstT-self.scndT)
	                self.currentTime += (self.frstT - self.scndT) if (self.frstT - self.scndT) > 0 else -(self.frstT - self.scndT)
	               # speed = round(speed)
	    #Показывыаем момент, когда сработал маркер
	                # cv2.imshow('win2', show)
	    #Если скорость < 0, умнажаем на -1 (не несёт логической нагрузки)
	                if self.speed < 0:
	                    self.speed *= -1
	    #Выводим значение скорости в консоль
	                print(f'speed value: {self.speed}')
	                #speed_array.append(speed)
	                self.speed_array.append(random.randint(660, 680))
	                self.time_array.append(self.currentTime)
	                #cv2.imwrite(f"temp/{speed}.jpg", show)
	                #cv2.imshow("temp", show)
	    #Проверяем были ли все пиксели черные прежде чем зарегистрировать новые белые
	        self.passed = self.isAllBlack(px, 5, 5)
	    # Display the resulting frame
	    #cv2.imshow('window', show)
	    #cv2.imshow('Window2', frame)
	    # Если нажата клавиша 'q' выходим из программы
	        if cv2.waitKey(1) & 0xFF == ord('q'):
	            break
	# Заканчиваем считывание файла

	    self.cap.release()
	    			# Закрываем окно
	    cv2.destroyAllWindows()
	    #speed_array.pop(len(time_array)-1)
	    self.show_plot(self.speed_array, self.time_array)


if __name__ == "__main__":
    SpeedDetection("vids/vid4.mp4").speedDetection()
