import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from fingerprint import pyenroll

kivy.require('1.8.0')


class RootWidget(BoxLayout):
    container = ObjectProperty(None)


class EzsApp(App):

    def build(self):
        self.root = Builder.load_file('kv/root.kv')

    def enroll(self, name):
        res = pyenroll.EnrollUser().inputFingerprint()
        print(res)
        if (res['res']):
            name.text = pyenroll.EnrollUser().getDecryptedText()
        else:
            self.open_popup(res['message'])

    # name.text = 'rpbon'
    # print(name)
    # print(self.ids.name.text)
    # self.ids.name = 'robin'
    # try:
    #     if (pyenroll.EnrollUser().input_finger_first_time()['res'] == True):
    #         if (pyenroll.EnrollUser().input_finger_second_time()['res'] == True):
    #             pyenroll.EnrollUser().save_fingerpring()
    #         else:
    #             self.open_popup('fingerpring dint match')
    #     else:
    #         self.open_popup('Something went wrong')
    # except Exception as e:
    #     print('Operation failed!')
    #     print('Exception message: ' + str(e))

    def open_popup(self, message):
        layout = GridLayout(cols=1, padding=20)
        popupLabel = Label(text=message)
        closeButton = Button(text="Close", pos_hint={'x': .1, 'top': .2}, size_hint=(.1, .1))
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)
        popup = Popup(title='Message', content=layout)
        popup.open()
        closeButton.bind(on_press=popup.dismiss)

    def register(self, file_name):
        self.changeUI(file_name)

    def login(self, username, password, file_name):
        self.changeUI(file_name)


    def changeUI(self, file_name):
        Builder.unload_file(file_name)
        self.root.clear_widgets()
        screen = Builder.load_file(file_name)
        self.root.add_widget(screen)

    def next_screen(self, screen):
        pyenroll.EnrollUser().enrollMe()


if __name__ == '__main__':
    '''Start the application'''
    EzsApp().run()
