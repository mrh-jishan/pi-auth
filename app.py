from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from fingerprint import pyenroll

import kivy

kivy.require('1.8.0')


class RootWidget(BoxLayout):
    container = ObjectProperty(None)


class EzsApp(App):
    def build(self):
        self.root = Builder.load_file('kv/root.kv')

    def enroll(self):
        pyenroll.EnrollUser().enrollMe()

    def login(self, username, password, file_name):
        Builder.unload_file(file_name)
        self.root.clear_widgets()
        screen = Builder.load_file(file_name)
        self.root.add_widget(screen)

    def next_screen(self, screen):
        pyenroll.EnrollUser().enrollMe()


if __name__ == '__main__':
    '''Start the application'''

    EzsApp().run()
