from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
import random

class Display(Widget):
    text = StringProperty()

    def change_text(self):
        self.text = str(random.randint(1, 100))

class MainApp(App):
    def build(self):
        return Display()

if __name__ == '__main__':
    obj=MainApp()
    obj.run()