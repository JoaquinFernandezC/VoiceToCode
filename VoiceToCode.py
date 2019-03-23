from pynput.keyboard import Key, Controller

import speech_recognition as sr

import os

from tkinter import *
import win32api
import win32con
import pywintypes

# GUI Window using Tkinter
window = Tk()
title = Label(text='VoiceToCode', font=('Times New Roman bold', '20'), fg='black', bg='white')
window.overrideredirect(1)
window.lift()
window.attributes("-topmost", True)
window.attributes("-disabled", True)
window.attributes("-alpha", 0.7)
window.geometry("-1+100")
hWindow = pywintypes.HANDLE(int(window.frame(), 16))
ex_style = win32con.WS_EX_COMPOSITED | \
          win32con.WS_EX_LAYERED | \
          win32con.WS_EX_NOACTIVATE | \
          win32con.WS_EX_TOPMOST | \
          win32con.WS_EX_TRANSPARENT
win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, ex_style)
title.pack()
#window.mainloop()

clear = lambda: os.system('cls')


def print_menu(current):
    if len(current) > 0:
        print(current[0] + ":")
        new_m = menu[current[0]]
        for i in current[1:]:
            new_m = new_m[i]
        for key, value in new_m.items():
            print(key)
    else:
        print('Select:')
        for key, value in menu.items():
            print(key)


recognizer = sr.Recognizer()
microphone = sr.Microphone()

keyboard = Controller()

# with microphone as source:
# recognizer.adjust_for_ambient_noise(source)


menu = {'make': {'for': 1, 'range': 2, 'variable': {'name variable': 1}},
        'jump': {'start': 1, 'up': 2, 'down': 3, 'end': 4}}

current_menu = ['start']
new_menu = []

while True:
    if current_menu != new_menu:
        clear()
        print_menu(new_menu)
        current_menu = new_menu[:]

    text = ""
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=2)
    try:
        text = recognizer.recognize_google(audio)
    except:
        pass

    if text != "":
        if text == "stop":
            break

        elif text == "print":
            pass
            # debug

        elif current_menu == []:
            if text == "make":
                new_menu.append("make")
            elif text == "jump":
                new_menu.append("jump")

        elif current_menu == ["make"]:
            if text == "for" or text == "4" or text == "four":
                keyboard.type("for i in :")
                keyboard.press(Key.left)
                new_menu = []
            elif text == "range":
                keyboard.type("range()")
                keyboard.press(Key.left)
                new_menu = []
            elif text == "bar":
                new_menu = ['make', 'variable']

        elif current_menu == ['make', 'variable']:
            keyboard.type(text.lower().replace(" ", "_") + " =")
            new_menu = []
        # print(text)
        text = ""

