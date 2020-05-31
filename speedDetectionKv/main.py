import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import  Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class SpeedDetectionApp(App):


    def build(self):

        '''
        Graphics initialization
        '''
        grLay = GridLayout(cols = 2, rows = 2)
        self.img = Image()
        self.speedLabel = Label()
        self.timeLabel = Label()
        #img = Image()
        #grLay.add_widget(Button(text = "Camera image will be here"))
        grLay.add_widget(self.img)
        grLay.add_widget(self.speedLabel)
        grLay.add_widget(Button(text = "TO DO:\nGraphics here"))
        grLay.add_widget(self.timeLabel)



        '''
        Speed detection params initialization
        '''
        self.cap = cv2.VideoCapture("../vids/vid5.mp4",0)
    #Проверяем вхождение времени
        self.first = True
        #Записываем время в переменные
        self.frstT = 0
        self.scndT = 0

        self.speed = 0
        self.passed = True
        # Количество лопастей
        self.n = 6

        self.speed_array = [0]
        self.time_array = list()


        '''
        Execution
        '''
        Clock.schedule_interval(self.update, 1.0/33)
        return grLay


    def update(self, dt):

        self.speedLabel.text = str(self.speed)
        tempTime = self.first - self.scndT
        self.timeLabel.text = str(tempTime)[8:13:1] if tempTime > 0 else str(-tempTime)[8:13:1]
        #frame = cv2.flip(self.speedDetection(),0)
        frame = self.speedDetection()
        # convert it to texture
        #buf1 = cv2.flip(frame, 0)
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='luminance')
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer.
        texture1.blit_buffer(buf, colorfmt='luminance', bufferfmt='ubyte')
        # display image from the texture
        self.img.texture = texture1

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
    #Resizing > color to gray > gray to binary
    #returning binary with thres threshold

        return cv2.threshold(cv2.cvtColor(cv2.resize(frame, (800, 600)),
                cv2.COLOR_BGR2GRAY), thres, 250, cv2.THRESH_BINARY)[1]

    def show_plot(self, speed_ax, time_ax):
        speed_ax = np.array(speed_ax)
        time_ax = np.array(time_ax)

        fig, ax = plt.subplots()
        ax.plot(time_ax, speed_ax)
        plt.show()

    def speedDetection(self):
        ret, frame = self.cap.read()


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
                self.speed = 360/(self.frstT-self.scndT)
                self.speed = round(self.speed)
    #Показывыаем момент, когда сработал маркер
                # cv2.imshow('win2', show)
    #Если скорость < 0, умнажаем на -1 (не несёт логической нагрузки)
                if self.speed < 0:
                    self.speed *= -1
    #Выводим значение скорости в консоль
                print(f'speed value: {self.speed}')
                self.speed_array.append(self.speed)
                #speed_array.append(random.randint(660, 680))
                self.time_array.append(time.time())
                #cv2.imwrite(f"temp/{speed}.jpg", show)
                #cv2.imshow("temp", show)
    #Проверяем были ли все пиксели черные прежде чем зарегистрировать новые белые
        self.passed = self.isAllBlack(px, 5, 5)
    # Display the resulting frame
    #cv2.imshow('window', show)
    #cv2.imshow('Window2', frame)
        return show

if __name__ == "__main__":
    SpeedDetectionApp().run()
