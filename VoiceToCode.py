from pynput.keyboard import Key, Controller

import pickle
import speech_recognition as sr
from threading import Thread
from tkinter import Tk, Label, StringVar, Canvas

import os,time

def openDic(name):
    try:
        with open(name+'.pickle','rb') as handle:
            dic=pickle.load(handle)
    except:
        dic={}
    return dic

def saveDic(name):
    with open(name+'.pickle', 'wb') as handle:
        pickle.dump(dics[name], handle, protocol=pickle.HIGHEST_PROTOCOL)

reserved=['False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
variables=[]

names=["print_dic","range_dic","stop_dic","for_dic", "make_dic", "variable_dic", "name_dic", "jump_dic", "start_dic", "up_dic", "down_dic", "end_dic"]
dics={"print":{},"stop":{},"for":{}, "make":{}, "variable":{}, "name":{}, "jump":{}, "start":{}, "up":{}, "down":{}, "end":{}}

variables=[]
words={}
for name in names:
    dics[name]=openDic(name)
    for el in dics[name]:  
        words[el]=name[0:-4]

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
        content_text=""
        var_name = voice_to_text("Enter var name",circle_canvas)
        if var_name in reserved:
           content_var.set("Variable is reserved")
        elif var_name in variables:
            content_var.set("Variable is used")
        else:
            variables.append(var_name)
            var_value=voice_to_text("Enter var value",circle_canvas)
            break
    keyboard.type(var_name.lower().replace(" ", "_") + " = "+var_value+"\n")

def use_variable(circle_canvas):
    while True:
        var_name=voice_to_text("Enter var name",circle_canvas)
        if var_name in reserved:
            #print("Variable is reserved")
            content_var.set("Variable is reserved")
        elif var_name not in variables:
            #print ("{} variable doesn't exist".format(var_name))
            content_var.set("{} variable doesn't exist".format(var_name))
        else:
           # print ("Variable Accepted")
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
                """
                if var_value:
                    keyboard.type("]")
                    keyboard.press(Key.enter)
                    break
                else:
                    """
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
                
                """
                var_value=var_name.split()
                if len(var_value)>1:
                    if var_value[0] in ["string","word"]:
                        var_value=var_value[1]
                    elif var_value[0] in ["number","int","integer"]:
                        try:
                            var_value=float(var_value[1])
                            lista.append(var_value)
                            #keyboard.type(var_value)
                        except:
                            var_value=voice_to_text("Enter element to add",circle_canvas)
                            continue
                """
                                    
                
                
                """
                var_value=voice_to_text("Enter element to add",circle_canvas)
                if var_value not in dics["stop_dic"]:
                    keyboard.type(', ')
                else:
                    keyboard.type("]")
                    keyboard.press(Key.enter)
                    break
                    #keyboard.type(var_value)
                """
            break
    


#clear()
#print_menu(current_menu)
def voice_recon(current_menu, circle_canvas):
    while True:
        text = ""
        menu_lenght = len(current_menu)
        content_text = ""
        content_var.set(content_text)
        print_menu(current_menu, content_text, content_var)
        with microphone as source:
            circle_canvas.itemconfig(circle, fill="green")
            audio = recognizer.listen(source,phrase_time_limit=3)
            
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
                text=words[text]
            if text in dics["stop_dic"]:
                window.destroy()
                break
                
            elif menu_lenght == 0:
                if text in menu:
                    if type(menu[text]) is dict:
                        current_menu.append(text)
                    else:
                        if text=="use variable":
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
                        if text=="variable":
                            menu_option[text](circle_canvas)
                        else:
                            menu_option[text]()
                        current_menu = []
                        
            #print(text)
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


menu = { 'make' : {'for': make_for,
                   'range': make_range,
                   'variable': make_var,
                   'print': make_print,
                   'list':make_list},
    
        'jump' : {'start':1,
                  'up':2,
                  'down':3,
                  'end':4},
        'use variable' : use_variable,
        
        'run': run_code,
        
        'undo': undo,
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
        
    
    