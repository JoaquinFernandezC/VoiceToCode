from pynput.keyboard import Key, Controller

import speech_recognition as sr

import os,time
clear = lambda: os.system('cls')

recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 50
recognizer.dynamic_energy_threshold = False

def voice_to_text(needed_text):
    text = ""
    print(needed_text)
    while True:
        with microphone as source:
            print("...")
            audio = recognizer.listen(source,phrase_time_limit=3)
        try:
            clear()
            print(needed_text)
            text = recognizer.recognize_google(audio)
            if text != "":
                break
        except:
            pass
    return text
    

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

def make_for():
    keyboard.type("for i in :")
    keyboard.press(Key.left)
    
def make_range():
    keyboard.type("range()")
    keyboard.press(Key.left)

def make_var():
    clear()
    var_name = voice_to_text("Enter var name")
    keyboard.type(var_name.lower().replace(" ", "_") + " =")


keyboard = Controller()

menu = { 'make' : {'for': make_for,
                   'range': make_range,
                   'bar': make_var},
    
        'jump' : {'start':1,
                  'up':2,
                  'down':3,
                  'end':4} }
current_menu = []
clear()
print_menu(current_menu)

while True:
    text = ""
    menu_lenght = len(current_menu)
    clear()
    print_menu(current_menu)
    with microphone as source:
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
                
            elif menu_lenght == 0:
                if text in menu:
                    current_menu.append(text)
            elif menu_lenght > 0:
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
                        
            #print(text)
            text = ""
    except:
        pass
    
    
    