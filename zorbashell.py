#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from os import path
import sys
import shutil
import os
import select
import subprocess
import re

from zorbacmd import ZorbaCMD
from zorbaspeech import ZorbaSpeech
from zorbachatter import ZorbaChatter

try:
    import gnureadline as readline
except ImportError:
    import readline
#from __future__ import braces #this makes it possible to use {} instead of indentation

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')

language = ''#'it-IT'

if language == '' and os.path.isfile("zorbalanguage.txt"):
    text_file = open("zorbalanguage.txt", "r")
    language = text_file.read().replace("\n", "")
    text_file.close()


Zorba = ZorbaCMD(language)

speech = ZorbaSpeech(language)

chatter = ZorbaChatter(language)
chatter.clearTraining()
chatter.train()

singlerun = False
continuous = True
voice = False

bot = 0
chat_id = 0

def sendMessage(chat_id, answer = "", voice = False):
    global bot
    global language
    
    if answer != "":
        if voice == True:
            #we should send audio
            newFileW = speech.speak(str(answer), str(chat_id))
            if chat_id > 0:
                bot.sendVoice(chat_id, open(newFileW, "rb"), caption = str(answer))
            else:
                os.system('aplay "' + newFileW + '"')
            if os.path.isfile(newFileW): os.remove(newFileW)
        else:
            if chat_id > 0:
                bot.sendMessage(chat_id, str(answer))
            else:
                print(str(answer))


for (i, item) in enumerate(sys.argv):
    if item == "-h":
        print("Options:\n -l specify language\n -p specify phrase to analize\n -c continuous mode, works as a shell (default)")
        
    if item == "-l":
        language = sys.argv[i+1]
        print("LANGUAGE: " + language)
        
    if item == "-p":
        singlerun = True
        
    if item == "-v":
        voice = True
        
    if item == "-c":
        singlerun = False
        continuous = True
        
        
while continuous:
    if voice == True:
        phrase = speech.recognize()
        print("You: " + phrase)
    else:
        phrase = input("You: ")
    phrases = list(filter(None, re.split("[;.!?]", phrase))) #if we've got multiple phrases, we split them
    for (p, itemp) in enumerate(phrases):
        command = phrases[p]
        if command != '':
            tr_cmd = Zorba.translate(command)
            if "SAYHELLO" == tr_cmd:
                res = "  ^_^\n"
                res = res + "(*.*)\n"
                res = res + "  ---"
                sendMessage(chat_id, res)
            elif "WHAT?" == tr_cmd:
                answer = chatter.reply(command)
                sendMessage(chat_id, str(answer), voice)
            elif "SET continuous FALSE" == tr_cmd:
                continuous = False
            else:
                cmdoutput = ""
                cmdoutput = subprocess.check_output(tr_cmd, shell=True).decode('UTF-8')
                print("OUTPUT:" + cmdoutput)
                if cmdoutput != "":
                    if cmdoutput[:8] == "photo://":
                        tmpfile = cmdoutput.replace("photo://", "")
                        tmpfile = tmpfile.replace("\n", "")
                        if os.path.isfile(tmpfile):
                            print(tmpfile)
                            os.system('w3m "' +tmpfile+'"')
                            os.remove(tmpfile)
                    elif cmdoutput[:4] == "Msg:":
                        msg = cmdoutput.replace("Msg:", "")
                        msg = msg.encode().decode('unicode_escape')
                        if str(msg) != '':
                            sendMessage(chat_id, str(msg), voice)
                else:
                    print(tr_cmd)
                    if singlerun == True:
                        continuous = False
