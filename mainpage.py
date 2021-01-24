import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from database import DataBase
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.image import Image
from kivy.uix.checkbox import CheckBox
from kivy.logger import Logger


# Registering new user
class CreateAccountWindow(Screen):
    phone = ObjectProperty()
    namee = ObjectProperty()
    password = ObjectProperty()
    status = ObjectProperty()
    address = ObjectProperty()

    def submit(self):
        length = len(self.phone.text)
        if self.namee.text != "" and self.phone.text != "" and self.status.text != "" and \
                length == 4 and self.address.text != "":
            if self.password.text != "":
                db.add_user(self.namee.text, self.password.text, self.phone.text, self.status.text, self.address.text)

                self.reset()
                winMan.current = "login"
            else:
                invalidForm()

        else:
            invalidForm()

    def login(self):
        self.reset()
        winMan.current = "login"

    def reset(self):
        self.phone.text = ""
        self.password.text = ""
        self.namee.text = ""
        self.status.text = ""
        self.address.text = ""


# Logging Existing User
class LoginWindow(Screen):
    password = ObjectProperty(None)
    phone = ObjectProperty(None)

    def loginButton(self):
        if db.validate(self.phone.text, self.password.text):
            MainWindow.current = self.phone.text
            self.reset()
            winMan.current = "main"
        else:
            invalidLogin()

    def createButton(self):
        self.reset()
        winMan.current = "create"

    def reset(self):
        self.password.text = ""
        self.phone.text = ""


class MainWindow(Screen):
    date = ObjectProperty(None)
    phone = ObjectProperty(None)
    name = ObjectProperty(None)
    value1 = ObjectProperty(None)
    value2 = ObjectProperty(None)
    value3 = ObjectProperty(None)

    def logOut(self):
        winMan.current = "login"

    def on_enter(self, *args):
        userdetail = db.get_user(self.current)
        if userdetail is not None:
            self.namee.text = userdetail[2]
            self.date.text = "" + str(userdetail[1])

    def checkbox_click1(self, check1, value1):
        self.value1 = value1

    def checkbox_click2(self, check2, value2):
        self.value2 = value2

    def checkbox_click3(self, check3, value3):
        self.value3 = value3

    def checkSelection(self):
        if self.value1 and self.value2 and self.value3:
            winMan.current = "form"
        else:
            unchecked()


class FormWindow(Screen):
    btnSymptom = ObjectProperty(None)
    namee = ObjectProperty(None)
    age: ObjectProperty(None)
    travel: ObjectProperty(None)
    fever: ObjectProperty(None)
    gender: ObjectProperty(None)

    Window.clearcolor = (1, 1, 1, 1)
    Window.size = (400, 600)

    def yourStatus(self):
        if self.namee.text != "" and self.age.text != "" and self.btnSymptom.text != "" and \
                self.fever.text != "" and self.travel.text != "":
            if int(self.fever.text) <= 99 and self.btnSymptom.text == "None of the above":
                winMan.current = "lowRiskScreen"
            else:
                winMan.current = "highRiskScreen"

class LowRiskStatus(Screen):

    def navigateCenterPage(self):
        winMan.current = "centerlist"

    def nextSteps(self):
        winMan.current = "lowRiskStep"

class NextStepsLowRisk(Screen):

    def backLowRisk(self):
        winMan.current = "lowRiskScreen"


class HighRiskStatus(Screen):
    pass

class NextStepsHighRisk(Screen):
    pass


class myImages(Screen):
    pass


class HelpCenters(Screen):
    data_items = ListProperty([])

    def on_enter(self, *args):
        centerList = db.getHelpline()
        for row in centerList:
            for col in row:
                print(col)
                self.data_items.append(col)

    def backLowRisk(self):
        winMan.current = "lowRiskScreen"


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(color=(1, 1, 1, 1), text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(color=(1, 1, 1, 1), text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def unchecked():
    pop = Popup(title='Invalid Form',
                content=Label(color=(1, 1, 1, 1), text='Please select all the options', bold=True),
                size_hint=(None, None), size=(400, 400))
    pop.open()


kv = Builder.load_file("login.kv")

winMan = WindowManager()
db = DataBase()

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main"),
           FormWindow(name="form"), HelpCenters(name="centerlist"), LowRiskStatus(name= "lowRiskScreen"),
           HighRiskStatus(name= "highRiskScreen"), NextStepsLowRisk(name="lowRiskStep"),
           NextStepsHighRisk(name="highRiskStep")]
for screen in screens:
    winMan.add_widget(screen)

winMan.current = "login"
# winMan.current = "lowRiskScreen"


class LoginApp(App):
    def build(self):
        return winMan


if __name__ == "__main__":
    LoginApp().run()
