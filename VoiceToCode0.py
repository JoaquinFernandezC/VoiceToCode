from pynput.keyboard import Key, Controller

import speech_recognition as sr

import os
import pickle
clear = lambda: os.system('cls')

reserved=['False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']

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
    


recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 50
recognizer.dynamic_energy_threshold = False

keyboard = Controller()

menu = { 'make' : {'for':1,'range':2,'variable': {'name variable':1}},
        'jump' : {'start':1,'up':2,'down':3,'end':4} }

current_menu = ['start']
new_menu = []

names=["range_dic","stop_dic","for_dic", "make_dic", "variable_dic", "name_dic", "jump_dic", "start_dic", "up_dic", "down_dic", "end_dic"]

dics={"for":{}, "make":{}, "variable":{}, "name":{}, "jump":{}, "start":{}, "up":{}, "down":{}, "end":{}}

variables=[]
for name in names:
    dics[name]=openDic(name)

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
            if text in dics["stop_dic"]:
                break
            
            elif text == "print":
                pass
                
                #debug
                
            elif current_menu == []:
                if text in dics["make_dic"]:
                    new_menu.append("make")
                elif text == "jump":
                    new_menu.append("jump")
                    
            elif current_menu == ["make"]:
                if text in dics["for_dic"]:
                    keyboard.type("for i in :")
                    keyboard.press(Key.left)
                    new_menu = []
                elif text in dics["range_dic"]:
                    keyboard.type("range()")
                    keyboard.press(Key.left)
                    new_menu = []
                elif text in  dics["variable_dic"]:
                    new_menu = ['make','variable']
                    
            elif current_menu == ['make','variable']:
                #keyboard.type(text.lower().replace(" ", "_") + " = ")
                #var=text
                
                while True:
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
                            if text!="":
                                if text in variables:
                                    print ("\nUSED VARIABLE\n")
                                    continue
                                else:
                                    print ("accepted variable")
                                    keyboard.type(text.lower().replace(" ", "_") + " = ")
                                    var=text
                                    while True:
                                        
                                        clear()
                                        print ("VARIABLE VALUE")
                                
                                        audio = recognizer.listen(source,phrase_time_limit=3)
                                        text = recognizer.recognize_google(audio)
                                        print("...")
                                        if text!="":       
                                            print ("accepted VALUE")
                                            keyboard.type(text.lower()+"\n")
                                            variables.append(var)
                                            break
                                
                                    break
                        except:
                            continue
                        break
                
                #for el in variables:
                 #   keyboard.type(el+"\n")
                new_menu = []
            print(text)
            text = ""
    except:
        pass
    
    
    