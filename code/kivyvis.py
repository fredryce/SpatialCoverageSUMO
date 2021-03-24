from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse, Line
import heatmapactual
from fdist import *
import numpy as np
from kivy.core.window import Window


class MyPaintWidget(Widget):

    global_dict = []
    temp_array = []

    def on_touch_down(self, touch):
        color = (random(), 1, 1)
        self.temp_array = []
        with self.canvas:
            Color(*color, mode='hsv')
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))


    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]
        self.temp_array.append([touch.x, touch.y])

    def on_touch_up(self, touch):
        print("adding a path")
        self.global_dict.append(np.array(self.temp_array))


class MyPaintApp(App):

    def build(self):
        layout = BoxLayout()
        #parent = Widget()
        self.painter = MyPaintWidget()
        clearbtn = Button(text='Clear', size_hint=(0.1, 0.1))
        clearbtn.bind(on_release=self.clear_canvas)
        compute_cov_button = Button(text="sp", size_hint=(0.1, 0.1))
        compute_cov_button.bind(on_release=self.compute_sp)


        spButton = Button(text="SP", size_hint=(0.1, 0.1))
        spButton.bind(on_release=self.compute_sp)
       
        layout.add_widget(self.painter)
        layout.add_widget(clearbtn)
        layout.add_widget(compute_cov_button)
        return layout

    def compute_sp(self, obj):
        route_dict = find_fdist(self.painter.global_dict[:-1])
        neqfunction(route_dict, factor_change=50)

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        self.painter.global_dict = []
        self.painter.temp_array = []
    def compute_spatial(self, obj):
        print(len(self.painter.global_dict))
        route_dict = find_fdist(self.painter.global_dict[:-1])
        #print(Window.size)

        total_cov = heatmapactual.diverse_calculation(route_dict, Window.size[0], Window.size[1])

        print(f"Total spatial coverage is ", total_cov)



if __name__ == '__main__':
    MyPaintApp().run()