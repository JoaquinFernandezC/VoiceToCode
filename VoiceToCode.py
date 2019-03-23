from pynput.keyboard import Key, Controller

import speech_recognition as sr

import os
clear = lambda: os.system('cls')

def print_menu(current):
    if len(current) > 0:
        print(current[0]+":")
        new_m = menu[current[0]]
        for i in current[1:]:
            new_m = new_m[i]
        for key, value in new_m.items() :
            print (key)
    else:
        print('Select:')
        for key, value in menu.items() :
            print (key)


recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 50
recognizer.dynamic_energy_threshold = False

keyboard = Controller()

menu = { 'make' : {'for':1,'range':2,'variable': {'name variable':1}},
        'jump' : {'start':1,'up':2,'down':3,'end':4} }

current_menu = ['start']
new_menu = []

while True:
    if current_menu != new_menu:
        current_menu = new_menu[:]
    
    text = ""
    with microphone as source:
        #recognizer.adjust_for_ambient_noise(source)
        clear()
        print_menu(current_menu)
        print("...")
        audio = recognizer.listen(source,phrase_time_limit=3)
        

    try:
        clear()
        print_menu(current_menu)
        text = recognizer.recognize_google(audio)
        if text != "":
            if text == "stop":
                break
            
            elif text == "print":
                pass
                
                #debug
                
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
                    new_menu = ['make','variable']
                    
            elif current_menu == ['make','variable']:
                keyboard.type(text.lower().replace(" ", "_") + " =")
                new_menu = []
            print(text)
            text = ""
    except:
        pass
    
    
    