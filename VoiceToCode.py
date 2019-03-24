from pynput.keyboard import Key, Controller
from threading import Thread

import speech_recognition as sr
import os
from tkinter import *


clear = lambda: os.system('cls')

recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 50
recognizer.dynamic_energy_threshold = False


def voice_to_text(needed_text, circle_canvas):
    text = ""
    content_text = ""
    content_text += (needed_text + '\n')
    content_var.set(content_text)


    while True:
        with microphone as source:
            circle_canvas.itemconfig(circle, fill="green")
            audio = recognizer.listen(source, phrase_time_limit=3)
        try:
            content_text = (needed_text + '\n')
            content_var.set(content_text)
            circle_canvas.itemconfig(circle, fill="red")
            text = recognizer.recognize_google(audio)
            if text != "":
                break
        except:
            pass
    return text


def print_menu(current, content_text, content_var):
    if len(current) > 0:
        content_text += (current[0] + ":\n")
        new_m = menu[current[0]]
        for i in current[1:]:
            new_m = new_m[i]
        for key, value in new_m.items():
            content_text += (key + '\n')
    else:
        content_text += 'Select:\n'
        for key, value in menu.items():
            content_text += (key + '\n')
    content_var.set(content_text)


def make_for():
    keyboard.type("for i in :")
    keyboard.press(Key.left)


def make_range():
    keyboard.type("range()")
    keyboard.press(Key.left)


def make_var():
    var_name = voice_to_text("Enter var name", circle_canvas)
    keyboard.type(var_name.lower().replace(" ", "_") + " =")


def voice_recon(current_menu, circle_canvas):
    while True:
        text = ""
        menu_length = len(current_menu)
        content_text = ""
        content_var.set(content_text)
        print_menu(current_menu, content_text, content_var)
        with microphone as source:
            circle_canvas.itemconfig(circle, fill="green")
            audio = recognizer.listen(source, phrase_time_limit=3)

        try:
            content_text = ""
            content_var.set(content_text)
            circle_canvas.itemconfig(circle, fill="red")
            print_menu(current_menu, content_text, content_var)
            text = recognizer.recognize_google(audio)
            if text != "":
                if text == "stop":
                    print("exiting...")
                    print("asd")
                    window.destroy()
                    break

                elif text == "print":
                    pass

                    # debug
                elif menu_length == 0:
                    if text in menu:
                        current_menu.append(text)
                elif menu_length > 0:
                    menu_option = menu[current_menu[0]]
                    for i in current_menu[1:]:
                        menu_option = menu_option[i]
                    if text in menu_option:
                        new_option = menu_option[text]
                        if type(new_option) is dict:
                            current_menu.append(text)
                        else:
                            menu_option[text]()
                            current_menu = []

                # print(text)
                text = ""
        except:
            pass
    print("hola")



# GUI Window using Tkinter
window = Tk()
content_text = ""
content_var = StringVar()
circle_canvas = Canvas(window, width=30, height=30, background='black', highlightthickness=0)
title = Label(text='VoiceToCode', font=('Courier New bold', '20'), fg='white', bg='black')
content = Label(textvariable=content_var, font=('Courier New', '15'), fg='white', bg='black')
window.overrideredirect(1)
window.attributes("-topmost", True)
window.attributes("-disabled", True)
window.attributes("-alpha", 0.7)
window.config(bg="black")
window.geometry("-1+100")

keyboard = Controller()

menu = {'make': {'for': make_for,
                 'range': make_range,
                 'bar': make_var},
    
        'jump': {'start': 1,
                 'up': 2,
                 'down': 3,
                 'end': 4}}
current_menu = []
content_var.set(content_text)
print_menu(current_menu, content_text, content_var)

title.pack()
circle_canvas.pack()
circle = circle_canvas.create_oval(10, 10, 20, 20, fill="red")
content.pack()
t = Thread(target=voice_recon, args=(current_menu, circle_canvas))
t.daemon = True
t.start()
window.mainloop()



