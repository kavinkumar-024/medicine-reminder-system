import pygame
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivy.clock import Clock
import datetime
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivy.app import App
from EasyThreadings import Thread
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from zqueue import Queue
from kivy.properties import StringProperty,ObjectProperty

pygame.init()

Window.size = (350, 600)

class HomeScreen(Screen):

    pass


class DateScreen(Screen):

    # click ok
    def on_save(self, instance, value, date_range):
        # print(instance,value,date_range)
        global lst
        lst=[]
        self.ids.date_label.text = "                saved successfully"
        lst = str(date_range).split("datetime.date(")
        lst.remove(lst[0])
        lst.remove(lst[len(lst) - 1])
        print(lst)

    # click cancel
    def on_cancel(self, instance, value):
        self.ids.date_label.text = "you clicked"
        # self.root.ids.date_label.text = str(date_range)

    def show_date_picker(self):
        date_dialog = MDDatePicker(mode='range')
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()




class TwoInputBox(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None,None)

        # create a horizontal box for the inputs
        input_box = BoxLayout(orientation='horizontal')

        # create the medication input and add it to the horizontal box
        self.medication_input = MDTextField(
            pos_hint = {'center_x':0.9,'center_y':0.9},
            hint_text='Medication name',
            multiline=False
        )
        input_box.add_widget(self.medication_input)

        # create the dosage input and add it to the horizontal box
        self.dosage_input = MDTextField(
            pos_hint = {'center_x':0.5,'center_y':0.2},
            hint_text='Units',
            multiline=False
        )
        input_box.add_widget(self.dosage_input)

        # add the horizontal box to the vertical box
        self.add_widget(input_box)

    def get_input(self):
        return self.medication_input.text.split(','), self.dosage_input.text.split(',')


class MenuScreen(Screen):
    global l, u,lp,dialog
    l = ['hello']
    u = [1]
    j=0
    lp=[]
    #dialog=0

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def on_enter(self, *args):
        try:
            if len(lst)==0:
                dialog = MDDialog(
                     title="FIX THE DATE",
                     buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda *args: dialog.dismiss()
                        )
                    ]
                )
                dialog.open()
        except:
            self.dialog = MDDialog(
                title="FIX THE DATE",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda *args: self.switch()
                    )
                ]
            )
            self.dialog.open()


    def switch(self,*args):
        self.app.root.current = 'home'
        self.dialog.dismiss()


    def user_input(self):
        # Create a dialog box with an input field and OK button
        dialog = MDDialog(
            # title="Enter medication details",
            type="custom",
            # size_hint = (0.8,0.8),
            content_cls=TwoInputBox(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda *args: dialog.dismiss()
                ),
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: self.process_input(dialog.content_cls.get_input(), dialog)
                ),
            ],
        )
        dialog.open()

    def process_input(self, input_text, dialog):
        # Use the input text however you want
        meds = input_text
        a, b = meds
        b = list(map(int, b))
        l.append(a)
        u.append(b)
        print(u)
        print(l)
        medu = dict(zip(a,b))
        lp.append(medu)
        print(lp)
        # Dismiss the dialog box
        dialog.dismiss()

    def list_items(self):
        layout = BoxLayout(orientation='vertical')
        label = MDLabel(text="Hello, world!", halign="center")
        layout.add_widget(label)

class details(Screen):

    def on_enter(self, *args):
        try:
            x = lp[0]
            self.formatted1_data = '\n'.join([f'{key} - {value}' for key, value in x.items()])
            self.ids.label1.text = "MORNING \n" + self.formatted1_data
        except:
            self.ids.label1.text='MORNING'
        try:
            x = lp[1]
            self.formatted2_data = '\n'.join([f'{key} - {value}' for key, value in x.items()])
            self.ids.label2.text = "MIDDAY \n" + self.formatted2_data
        except:
            self.ids.label2.text='MIDDAY'
        try:
            x = lp[2]
            self.formatted3_data = '\n'.join([f'{key} - {value}' for key, value in x.items()])
            self.ids.label3.text = "EVENING \n" + self.formatted3_data
        except:
            self.ids.label3.text='EVENING'
        try:
            x = lp[3]
            self.formatted4_data = '\n'.join([f'{key} - {value}' for key, value in x.items()])
            self.ids.label4.text = "NIGHT \n" + self.formatted4_data
        except:
            self.ids.label4.text='night'


class ResetScreen(Screen):
    def __init__(self, **kwargs):
        super(ResetScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def reset(self):
        try:
            l=['hi']
            li.clear()
            lst.clear()
            u=[1]
            lp.clear()
            self.ids.rest_label.text = "resetted succesfully"
            self.app.root.current = 'home'
        except:
            self.dialog = MDDialog(
                title="check the datas",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda *args: self.switch()
                    )
                ]
            )
            self.dialog.open()


    def switch(self):
        self.app.root.current = 'menu'
        self.dialog.dismiss()

class More_screen(Screen):
    pass



class Add_units(Screen):

    change=0

    def __init__(self, **kwargs):
        super(Add_units, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def on_enter(self, *args):
        pass

    def spinner_clicked(self,value):
        global a
        self.ids.click_label.text = value
        if self.ids.click_label.text=='Morning':
            a=0
        elif self.ids.click_label.text=='Midday':
            a=1
        elif self.ids.click_label.text=='Evening':
            a=2
        elif self.ids.click_label.text=='Night':
            a=3




    def on_button_click(self):
        dialog = MDDialog(
            type="custom",
            content_cls=TwoInputBox(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda *args: dialog.dismiss()
                ),
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: [self.process_input(dialog.content_cls.get_input(), dialog),dialog.dismiss()]
                ),
            ],
        )
        dialog.open()

    def process_input(self, input_text, dialog):
        try:
            meds = input_text
            c, b = meds
            b = list(map(int, b))
            di = {k: v for k, v in zip(c, b)}
            lp[a]=di
            print(lp)

            # Set the label's text to the new value
            self.ids.my_label.text = str(di)
        except:
            self.dialog = MDDialog(
                title="",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda *args: self.switch()
                    )
                ]
            )
            self.dialog.open()

    def switch(self):
        self.app.root.current='menu'
        self.dialog.dismiss()






class AlarmScreen(Screen):
    picked_time = None  # initialize global variable

    def time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time, on_save=self.save_time)
        time_dialog.open()

    def save_time(self, instance, time):
        global li
        self.picked_time = time  # save the picked time in the global variable
        li = []
        a = self.picked_time
        a = str(a)
        li.append(a)
        print(li)

    def get_time(self, instance, time):
        self.ids.alarm_time.text = str(time)


from kivy.clock import Clock


class Alarm(Screen):
    meds=[]
    uni=[]
    i = 0
    pygame.init()
    sound = pygame.mixer.Sound('Medicine Reminder - Pill Reminder.mp3')
    volume = 0
    j = 0
    program_running = False
    z=0

    def __init__(self, **kwargs):
        super(Alarm, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def on_enter(self):
        if not self.program_running:
            if self.j == 1:
                Clock.schedule_once(self.start_alarm, 60)
            else:
                self.start_alarm()

    def start_alarm(self, *args):
        self.program_running = True
        self.program_thread = Thread(target=self.alarm)
        self.program_thread.start()

    def on_leave(self):
        # Stop running the program when leaving the screen
        pass

    def alarm(self, *args):
        # global i
        try:
            now = datetime.datetime.now()

            formatted_date = "{}, {}, {}".format(now.year, now.month, now.day)

            a = formatted_date

            b = str(a)
            c = b[:11]
            # print(c)
            d = c.replace('-', ', ')
            d = d + "), "
            while d in lst:
                now = datetime.datetime.now().time()
                formatted_time = datetime.time(now.hour, now.minute)
                if str(formatted_time) in li:

                    print(formatted_time)
                    self.z=li.index(str(formatted_time))
                    print(self.z)
                    self.start()
                    #self.i = self.i + 1
                    x=lp[self.z]
                    self.meds=list(x.keys())
                    self.uni=list(x.values())
                    k = []
                    for j in self.uni:
                        j = j - 1
                        k.append(j)
                    self.uni=k


                    #print(self.i)
                    Clock.schedule_once(self.pop)
                    break
        except:
            Clock.schedule_once(self.exce)

    def pop(self, *args):
        global title_str
        di = {k: v for k, v in zip(self.meds, self.uni)}
        lp[self.z]=di
        title_str = ", ".join("{}: {} units".format(k, v) for k, v in di.items())

        self.dialog = MDDialog(
            title='MEDICINES' + '\n' + title_str,
            type="custom",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: self.off()
                ),
            ],
        )
        self.dialog.open()
        # i = i+1

    def off(self):
        self.stop()
        self.dialog.dismiss()

    def exce(self, *args):
        self.dialog = MDDialog(
            title='CHECK YOU HAVE FIX THE DATE OR TIME CORRECTLY',
            type="custom",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: self.switch()
                )
            ]
        )
        self.dialog.open()

    def switch(self,*args):
        self.app.root.current='menu'
        self.dialog.dismiss()


    def cancel_dialog(self, dialog):
        dialog.dismiss()
        # time.sleep(60)
        self.j = 1
        self.program_running = False
        self.on_enter()

        # Wait for the dialog to be fully dismissed before proceeding
        # while dialog._window.do_layout:
        # time.sleep(0.1)

    def set_volume(self, *args):
        self.volume += 0.1
        if self.volume < 1.0:
            Clock.schedule_interval(self.set_volume, 10)
            self.sound.set_volume(self.volume)
            # print(self.volume)
        else:
            self.sound.set_volume(1)
            # print("rich max volume")

    def start(self, *args):
        self.sound.play(-1)
        self.set_volume()

    def stop(self):
        self.sound.stop()
        self.volume = 0
        # time.sleep(60)
        # self.on_enter()
        self.program_running = False


class Alarm1Screen(Screen):
    picked_time = None  # initialize global variable

    def time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time, on_save=self.save_time)
        time_dialog.open()

    def save_time(self, instance, time):
        self.picked_time = time  # save the picked time in the global variable
        a = self.picked_time
        a = str(a)
        li.append(a)
        print(li)

    def get_time(self, instance, time):
        self.ids.alarm_time.text = str(time)


class Alarm2Screen(Screen):
    picked_time = None  # initialize global variable

    def time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time, on_save=self.save_time)
        time_dialog.open()

    def save_time(self, instance, time):
        self.picked_time = time  # save the picked time in the global variable
        a = self.picked_time
        a = str(a)
        li.append(a)
        print(li)

    def get_time(self, instance, time):
        self.ids.alarm_time.text = str(time)


class Alarm3Screen(Screen):
    picked_time = None  # initialize global variable

    def time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time, on_save=self.save_time)
        time_dialog.open()

    def save_time(self, instance, time):
        self.picked_time = time  # save the picked time in the global variable
        a = self.picked_time
        a = str(a)
        li.append(a)
        print(li)

    def get_time(self, instance, time):
        self.ids.alarm_time.text = str(time)


sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(DateScreen(name='Date'))
sm.add_widget(AlarmScreen(name='alarm'))
sm.add_widget(Alarm(name='remain'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(Alarm1Screen(name='alarm1'))
sm.add_widget(ResetScreen(name='reset'))
sm.add_widget(Add_units(name='units'))
sm.add_widget(Alarm2Screen(name='alarm2'))
sm.add_widget(Alarm3Screen(name='alarm3'))
sm.add_widget(details(name='data'))
sm.add_widget(More_screen(name='more'))


# sm.add_widget(Alarm1(name='remain1'))
# sm.add_widget(CustomPopup(name='pop'))


class Remainder(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('main.kv')


Remainder().run()
