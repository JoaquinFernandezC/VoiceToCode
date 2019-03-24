from pynput.keyboard import Key, Controller

import pickle
import speech_recognition as sr
from threading import Thread
from tkinter import Tk, Label, StringVar, Canvas

def open_dic(name):
    try:
        with open('dic_picks\\' + name+'.pickle', 'rb') as handle:
            dic = pickle.load(handle)
    except:
        dic = {}
    return dic


def save_dic(name):
    with open(name+'.pickle', 'wb') as handle:
        pickle.dump(dics[name], handle, protocol=pickle.HIGHEST_PROTOCOL)


reserved = ['False', 'None', 'True', 'and', 'as', 'assert', 'back', 'break',
            'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
            'exec', 'finally', 'for', 'from', 'global', 'if', 'import', 'in',
            'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
            'try', 'while', 'with', 'yield']

variables = []
functions = []

names = ["print_dic","run_dic","range_dic","for_dic", "make_dic", "variable_dic", 
         "name_dic", "jump_dic", "move_dic", "start_dic", "up_dic", "down_dic", 
         "left_dic", "right_dic", "end_dic", "stop_dic"]
dics = {"print":{},"run":{},"range":{},"for":{}, "make":{}, "variable":{}, "name":{},
        "jump":{}, "move":{}, "start":{},  "up":{}, "down":{}, "left":{}, "right":{},
        "end":{}, "stop":{}}

variables = []
words = {}
for name in names:
    dics[name] = open_dic(name)
    for el in dics[name]:
        words[el] = name[0:-4]

recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 30
recognizer.dynamic_energy_threshold = False


def voice_to_text(needed_text, circle_canvas):
    text = ""
    content_text = ""
    content_text += (needed_text + '\n')
    content_var.set(content_text)
    while True:
        with microphone as source:
            circle_canvas.itemconfig(circle, fill="green")
            audio = recognizer.listen(source, phrase_time_limit=2)
        try:
            content_text = (needed_text + '\n')
            content_var.set(content_text)
            circle_canvas.itemconfig(circle, fill="red")
            text = recognizer.recognize_google(audio)
        except:
            pass
        if text != "":
                break
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
    if 'element' not in variables:
        variables.append('element')
    keyboard.type("for element in :")
    keyboard.press(Key.left)


def make_range():
    keyboard.type("range()")
    keyboard.press(Key.left)


def make_var(circle_canvas):
    while True:
        var_name = voice_to_text("Enter var name", circle_canvas)
        if var_name == "back":
            return
        if var_name in reserved:
            content_var.set("Variable is reserved")
        elif var_name in variables:
            content_var.set("Variable is used")
        else:
            variables.append(var_name)
            var_value = voice_to_text("Enter var value", circle_canvas)
            break
    try:
        float(var_value)
    except ValueError:
        var_value = "\"" + var_value + "\""
    keyboard.type(var_name.lower().replace(" ", "_") + " = "+var_value+"\n")


def make_function(circle_canvas):
    while True:
        function_name = voice_to_text("Enter function name", circle_canvas)
        if function_name == "back":
            return
        if function_name in reserved:
            content_var.set("Function is reserved")
        elif function_name in functions:
            content_var.set("Function already defined")
        else:
            functions.append(function_name)
            break
    keyboard.type("def " + function_name.lower().replace(" ", "_") + "():\n pass")
    keyboard.press(Key.enter)


def use_variable(circle_canvas):
    while True:
        var_name = voice_to_text("Enter var name",circle_canvas)
        if var_name in reserved:
            content_var.set("Variable is reserved")
        elif var_name not in variables:
            content_var.set("{} variable doesn't exist".format(var_name))
        else:
            content_var.set("Variable Accepted")
            keyboard.type(var_name.lower())
            keyboard.press(Key.end)
            keyboard.press(Key.enter)
            break
        

def run_code():
    keyboard.press(Key.f5)


def make_print():
    keyboard.type("print(")
    #keyboard.press(Key.left)


def undo():
    keyboard.press(Key.ctrl)
    keyboard.press('z')
    keyboard.release(Key.ctrl)
    keyboard.release('z')


def make_list():
    while True:
        content_text=""
        var_name = voice_to_text("Enter list name",circle_canvas)
        if var_name in reserved:
           content_var.set(var_name+" is reserved")
        elif var_name in variables:
            content_var.set(var_name+" is used")
        else:
            variables.append(var_name)
            keyboard.type(var_name+' = [')
            var_value=voice_to_text("Enter element to add",circle_canvas)
            lista=[]
            while True:
                content_text=""
                try: 
                    var_value=float(var_value)
                except:
                    try: 
                        var_value=str(var_value)
                    except:
                        var_value=voice_to_text("Enter element to add",circle_canvas)
                        continue
                if type(var_value)==str:
                    lista.append("'"+var_value+"'")
                else:
                    lista.append(str(var_value))
                listaFinal=','.join(lista)
                print ("HELLO")
                var_value=voice_to_text("Enter element to add"+"\n"+listaFinal,circle_canvas)
                if var_value in dics["stop_dic"]:
                        lista=','.join(lista)
                        keyboard.type(lista)
                        keyboard.press(Key.right)
                        keyboard.press(Key.enter)
                        break
                else:
                    continue
            break
    

def move_start():
    keyboard.press(Key.home)


def move_end():
    keyboard.press(Key.end)


def move_down():
    keyboard.press(Key.down)
    

def move_left():
    keyboard.press(Key.left)
    

def move_right():
    keyboard.press(Key.right)
    

def move_up():
    keyboard.press(Key.up)


def manual(circle_canvas):
    while True:
        var_name = voice_to_text("Dictate \n or stop", circle_canvas)
        if var_name in dics["stop_dic"]:
            break
        if var_name == "enter":
            keyboard.press(Key.enter)
        elif var_name != '':
            keyboard.type(var_name)


def voice_recon(current_menu, circle_canvas):
    while True:
        text = ""
        menu_lenght = len(current_menu)
        content_text = ""
        content_var.set(content_text)
        print_menu(current_menu, content_text, content_var)
        with microphone as source:
            circle_canvas.itemconfig(circle, fill="green")
            audio = recognizer.listen(source, phrase_time_limit=2)

        try:
            content_text = ""
            content_var.set(content_text)
            circle_canvas.itemconfig(circle, fill="red")
            print_menu(current_menu, content_text, content_var)
            text = recognizer.recognize_google(audio)
        except:
            pass
        
        if text != "":
            if text in words:
                text = words[text]
            if text in dics["stop_dic"]:
                window.destroy()
                break
            elif text == "back":
                current_menu.pop()
            elif menu_lenght == 0:
                if text in menu:
                    if text == 'move':
                        while True:
                            content_text = "Enter direction\nto move cursor \nor stop:\n"
                            for key in menu['move']:
                                content_text += key+'\n'
                            new_direction = voice_to_text(content_text, circle_canvas)
                            if new_direction in words:
                                new_direction = words[new_direction]
                            if new_direction in dics["stop_dic"]:
                                break
                            elif new_direction in menu['move']:
                                menu['move'][new_direction]()
                        current_menu = []
                    elif type(menu[text]) is dict:
                        current_menu.append(text)
                    else:
                        if text == "use variable" or text == 'manual':
                            menu[text](circle_canvas)
                        else:
                            menu[text]()
            elif menu_lenght > 0:
                menu_option = menu[current_menu[0]]
                for i in current_menu[1:]:
                    menu_option = menu_option[i]
                if text in menu_option:
                    new_option = menu_option[text]
                    if type(new_option) is dict:
                        current_menu.append(text)
                    else:
                        if text == "variable" or text == "function":
                            menu_option[text](circle_canvas)
                        else:
                            menu_option[text]()
                        current_menu = []
            text = ""

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
                 'variable': make_var,
                 'print': make_print,
                 'function': make_function,
                 'list':make_list},
        'move': {'start': move_start,
                 'left': move_left,
                 'right': move_right,
                 'up': move_up,
                 'down': move_down,
                 'end': move_end},
        'manual': manual,
        'use variable': use_variable,
        'run': run_code,
        'undo': undo
        }
        
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
