import time

import kivy
from firebase import firebase
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
        self.firebase = firebase.FirebaseApplication('https://attendance-system-51f12.firebaseio.com/', None)
        self.pyfinger = pyenroll.EnrollUser()
        self.root = Builder.load_file('kv/root.kv')

    def enroll(self, name):
        res = self.pyfinger.inputFingerprint()
        print(res)
        if res['res'] == False:
            self.changeUI('kv/register.kv')
        else:
            self.open_popup(res['message'])

    def deletUser(self):
        res = self.pyfinger.inputFingerprint()
        if res['res'] == True:
            print(res)
            if self.pyfinger.f.deleteTemplate(res['pos']) == True:
                self.open_popup('User deleted successfully')
            else:
                self.open_popup('Something went wrong! Try again')
        else:
            self.open_popup('Sorry! User not found')

    def open_popup(self, message):
        layout = GridLayout(cols=1, padding=20)
        popupLabel = Label(text=message)
        closeButton = Button(text="Close", pos_hint={'x': .1, 'top': .2}, size_hint=(.1, .1))
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)
        popup = Popup(title='Message', content=layout)
        popup.open()
        closeButton.bind(on_press=popup.dismiss)

    def registerStudents(self, email, name, role):
        uuid = self.pyfinger.save_fingerpring()
        data = {'name': name, 'uuid': uuid, 'role': role, 'email': email}
        result = self.firebase.post('/users/', data)
        if (result):
            self.open_popup('User added successfully!')
            self.changeUI('kv/home.kv')

    def login(self):
        data = self.firebase.get('/users/', '')
        res = self.pyfinger.inputFingerprint()
        isAdmin = False


        print(res)
        print(data)

        if res['res'] == True:
            for k in data:
                if data[k]['role'] == 'admin' and res['pos'] == data[k]['uuid']:
                    isAdmin = True
            if isAdmin:
                self.changeUI('kv/home.kv')
            else:
                self.open_popup('Sorry! you are not admin')
        else:
            self.open_popup('Sorry! We cound\'t find the user. Please try again.')

    def changeUI(self, file_name):
        Builder.unload_file(file_name)
        self.root.clear_widgets()
        screen = Builder.load_file(file_name)
        self.root.add_widget(screen)


if __name__ == '__main__':
    '''Start the application'''
    EzsApp().run()
