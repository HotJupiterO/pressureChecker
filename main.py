# C:\Users\yrepe\AppData\Local\Programs\Python\Python37\share\kivy-examples\demo\kivycatalog   - path to kivy-examples
from kivy import Config

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'minimum_width', '1100')
Config.set('graphics', 'minimum_height', '600')

import random
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np
import requests
import csv


class MyGrid(BoxLayout):
    def __enter__(self):
        pass

    # global var for stopwatch
    old_sec = 0
    m = 0
    h = 0

    number = NumericProperty()
    value_list = []

    def set_cur_time(self):
        self.cur_time.text = time.strftime('%H:%M:%S')

    def start_clock(self):
        Clock.schedule_interval(lambda f: self.set_cur_time(), 1)

    def start_(self):
        self.old_sec = time.time()
        self.start()
        self.stopwatch()

    def start(self):
        self.rejestracjadanych.text = 'Aktywna'
        self.plt.clear_widgets(children=None)
        # val = self.get_val_from_url(self, url)
        val = random.randint(9, 15)
        self.putIntoCSV(val, 'test.csv')
        self.value_list.append(val)
        plt.plot(self.value_list)
        plt.ylabel('%')
        plt.xlabel('Time')
        self.plt.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        interval = 10
        self.interwal.text = str(interval) + ' sec'
        Clock.schedule_once(lambda f: self.start(), interval)

    def set_short(self):
        self.plt.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def get_val_from_url(self, url):
        val = requests.get(url)
        self.putIntoCSV(val)
        self.value_list.append(val)

    def get_rand_val(self):
        val = random.randint(1, 15)
        self.value_list.append(val)
        return val

    def putIntoCSV(self, val, csv_path):
        with open(csv_path, 'a') as f:
            writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([time.strftime('%H:%M:%S'), val])

    def time_from_start(self):
        cur_sec = int(time.time() - self.old_sec)
        if cur_sec > 59:
            self.m = + 1
            cur_sec = 0
            self.old_sec = time.time()
        if self.m > 59:
            self.h = + 1
            self.m = 0
        self.stopwatch_.text = '{}:{}:{} [h:m:s]'.format(str(self.h), str(self.m), str(cur_sec))

    def stopwatch(self):
        Clock.schedule_interval(lambda f: self.time_from_start(), 1)


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == '__main__':
    MyApp().run()
