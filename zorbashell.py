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


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



try:
    import gnureadline as readline
except ImportError:
    import readline
#from __future__ import braces #this makes it possible to use {} instead of indentation

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')


DIRECTORY_TO_WATCH = os.path.abspath(os.path.dirname(sys.argv[0])) + "/watchme/"
language = ''#'it-IT'
singlerun = False
continuous = True
voice = False

bot = []
chat_id = ""



if language == '' and os.path.isfile("zorbalanguage.txt"):
    text_file = open("zorbalanguage.txt", "r")
    language = text_file.read().replace("\n", "")
    text_file.close()

Zorba = ZorbaCMD(language)
speech = ZorbaSpeech(language)

chatter = ZorbaChatter(language)
chatter.clearTraining()
chatter.train()



class zwHandler(FileSystemEventHandler):
    global bot
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        #elif event.event_type == 'created':
        elif event.event_type == 'modified':
            try:
                Zorba.set_telegramusers(listusers())
            except:
                nousers = True
            if os.path.isfile(event.src_path):
                content = ""
                text_file = open(event.src_path, "r")
                content = text_file.read().replace("\n", "")
                text_file.close()
                if content[:4] == "CMD:":
                    tr_cmd = Zorba.translate(content.replace("CMD:", ""))
                    if "WHAT?" == tr_cmd:
                        answer = chatter.reply(content)
                        Zorba.sendMessage(chat_id, bot, speech, str(answer), voice, "")
                    else:
                        try:
                            cmdoutput = subprocess.check_output(tr_cmd, shell=True).decode('UTF-8')
                        except:
                            cmdoutput = ""
                        if cmdoutput != "":
                            Zorba.display_output(cmdoutput, "", bot, speech, voice)
                        else:
                            print(tr_cmd)
                else:
                    Zorba.display_output(content, "", bot, speech, voice)
                if os.path.isfile(event.src_path): os.remove(event.src_path)
            

for (i, item) in enumerate(sys.argv):
    if item == "-h":
        print("Options:\n -l specify language\n -p specify phrase to analize\n -c continuous mode, works as a shell (default)\n -v uses voice recognition and sinthesys")
        
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
        
observer = Observer()
event_handler = zwHandler()
observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
observer.start()
        
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
                #sendMessage(chat_id, res)
                Zorba.sendMessage(chat_id, bot, speech, res)
            elif "WHAT?" == tr_cmd:
                answer = chatter.reply(command)
                Zorba.sendMessage(chat_id, bot, speech, str(answer), voice)
            elif "SET continuous FALSE" == tr_cmd:
                continuous = False
            else:
                try:
                    cmdoutput = subprocess.check_output(tr_cmd, shell=True).decode('UTF-8')
                except:
                    cmdoutput = ""
                if cmdoutput != "":
                    Zorba.display_output(cmdoutput, "", bot, speech, voice)
                else:
                    print(tr_cmd)
                    if singlerun == True:
                        continuous = False

observer.stop()
observer.join()
