# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 15:35:19 2019

@author: Felipe
"""

import speech_recognition as sr


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
    

import os
clear = lambda: os.system('cls')

import pickle

recognizer = sr.Recognizer()
microphone = sr.Microphone()

names=["print_dic","run_dic","range_dic","for_dic", "make_dic", "variable_dic", "name_dic", "jump_dic", "start_dic", "up_dic", "down_dic", "end_dic"]

dics={"print":{},"run":{},"for":{}, "make":{}, "variable":{}, "name":{}, "jump":{}, "start":{}, "up":{}, "down":{}, "end":{}}

for name in names:
    dics[name]=openDic(name)


text=""
#stop_dic=[]
#make_dic=[]

#stop_dic=openDic(stop_dic,"stop_dic")
#make_dic=openDic(make_dic,"make_dic")
name="print_dic"
dics[name]=openDic(name)
stop_dic=openDic("stop_dic")

#del dics["for_dic"]["endd"]
print (dics[name])
#for_dic=openDic(for_dic,"for_dic")
while True:
    #dics[name]["stop"]=1
    #break    
    #del dics[name]["up"]
    dics[name]["parent"]=1
    break
    print ("TRAINING",name+"\n")
    with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            clear()
            #print_menu(new_menu)
            audio = recognizer.listen(source,phrase_time_limit=2)
            print("...")
    try:
        text=recognizer.recognize_google(audio)
        print (text)
    except:
        pass
    if text in stop_dic:
        break
    else:
        if text in dics[name]:
            dics[name][text]+=1
        else:
            if text!="":
                dics[name][text]=1
    
saveDic(name)
#saveDic(make_dic,"make_dic")
#saveDic(stop_dic,"stop_dic")
print(dics[name])