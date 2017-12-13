#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Run this code with python3.5
#

#-ocr image from telegram photo https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#fetch-images-sent-to-your-bot
#updates = bot.get_updates()
#>>> print([u.message.photo for u in updates if u.message.photo])
#http://telepot.readthedocs.io/en/latest/reference.html


import time
import random
import datetime
import telepot
import os
import sys
import subprocess
from zorbacmd import ZorbaCMD
from zorbaspeech import ZorbaSpeech
from zorbachatter import ZorbaChatter

telegramtoken = '' #telegram bot token from BotFather
checkuserid = 1 #enable users whitelist, so only certain people can talk with this bot
usersfile = 'botusers.csv' #the file where we store the list of users who can talk with bot
attemptsfile = '/tmp/attempts.log' #the file where we log denied accesses
active = 1 #if set to 0 the bot will stop
ocrlang = ''
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

if telegramtoken == '' and os.path.isfile("telegramtoken.txt"):
    text_file = open("telegramtoken.txt", "r")
    telegramtoken = text_file.read().replace("\n", "")
    text_file.close()

print("Connecting to Telegram...")
bot = telepot.Bot(telegramtoken)
print(bot.getMe())



def getocrlang():
    global language
    global ocrlang
    
    #NOTE: this si just an hack, probably it's better to build a translation array
    cmdoutput = subprocess.check_output("tesseract --list-langs", shell=True).decode('UTF-8')
    tesseractlangs = cmdoutput.split("\n")
    for i in range(len(tesseractlangs)):
        if tesseractlangs[i][:2] == language[:2]:
            ocrlang = tesseractlangs[i]
    if ocrlang == "":
        ocrlang = "eng"
    return ocrlang

    
def listusers():
    if not os.path.isfile(usersfile):
        return ''
    text_file = open(usersfile, "r")
    lines = text_file.read().split(',')
    text_file.close()
    del lines[-1] #remove last element since it is blank
    return lines

def adduser(name):
    global checkuserid
    
    csv = ""
    users = listusers()
    if users != "":
        for usr in users:
            csv = csv+usr+","
    if name not in csv:
        csv = csv+name+","
    text_file = open(usersfile, "w")
    text_file.write(csv)
    text_file.close()
    
def deluser(name):
    csv = ""
    users = listusers()
    if users != "":
        for usr in users:
            if usr != name:
                csv = csv+usr+","
    text_file = open(usersfile, "w")
    text_file.write(csv)
    text_file.close()
    
def sendMessage(chat_id, answer = "", voice = False):
    global bot
    global language
    global ocrlang
    
    if answer != "":
        if voice == True:
            #we should send audio
            newFileW = speech.speak(str(answer), str(chat_id))
            #os.system('espeak -s 150 -p 50 -w ' + newFileW + ' "' + str(answer) + '"')
            bot.sendVoice(chat_id, open(newFileW, "rb"), caption = str(answer))
            if os.path.isfile(newFileW): os.remove(newFileW)
        else:
            bot.sendMessage(chat_id, str(answer))

def handle(msg):
    global bot
    global chatter
    global language
    global checkuserid
    
    chat_id = msg['chat']['id']
    sender = msg['from']['id']

    users = listusers()
    if len(users) < 1:
        checkuserid = 0
    else:
        checkuserid = 1


    if checkuserid == 1:
        verified = 0
        if users != "":
            for usr in users:
                if str(sender) == usr:
                    verified = 1
        if verified == 0:
            sendMessage(chat_id, "I don't talk with strangers, dear "+str(sender))
            #write this user in the list of attempted accesses
            if attemptsfile != '':
                lines = ''
                if os.path.isfile(attemptsfile):
                    text_file = open(attemptsfile, "r")
                    lines = text_file.read()
                    text_file.close()
                lines = lines + str(datetime.datetime.now()) + " --- UserdID: " + str(sender) + " DENIED \n"
                text_file = open(attemptsfile, "w")
                text_file.write(lines)
                text_file.close()
            return
    
    command = ''
    
    voice = False
    
    try:
        if msg['voice'] != '':
            voice = True
    except:
        voice = False
    
    if voice == True:
        file_id = msg['voice']['file_id']
        tmpfile = str(datetime.datetime.now()).replace(" ","_").replace(":","_")
        newFileO = "/tmp/voice" + tmpfile + "_" + str(sender) + ".ogg"
        newFileW = "/tmp/voice" + tmpfile + "_" + str(sender) + ".wav"
        bot.download_file(file_id, newFileO)
        #http://telepot.readthedocs.io/en/latest/reference.html
        os.system("ffmpeg -i " + newFileO + " -acodec pcm_s16le -ac 1 -ar 16000 "+ newFileW)
        if os.path.isfile(newFileW):
            speech.setAudioFile(newFileW)
            command = speech.recognize()
            print("Recognized: " + command)
        if os.path.isfile(newFileO): os.remove(newFileO)
        if os.path.isfile(newFileW): os.remove(newFileW)
    
    #print(msg)
    photo = False
    try:
        if msg['photo'] != '':
            photo = True
    except:
        photo = False
    
    if photo == True:
        i = len(msg['photo'])-1
        file_id = msg['photo'][i]['file_id']
        tmpfile = str(datetime.datetime.now()).replace(" ","_").replace(":","_")
        newFileJ = "/tmp/photo" + tmpfile + str(i) + "_" + str(sender) + ".jpg"
        newFileT = "/tmp/photo" + tmpfile + str(i) + "_" + str(sender) + ".txt"
        bot.download_file(file_id, newFileJ)
        #TODO: convert language from standard en-US
        if ocrlang == "":
            getocrlang()
        os.system("tesseract -l " + ocrlang + " -psm 3 " + newFileJ + " " + newFileT[:-4]) #psm7 is better? https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage
        if os.path.isfile(newFileT):
            text_file = open(newFileT, "r")
            lines = text_file.read()
            text_file.close()
            if lines != "":
                sendMessage(chat_id, str(lines), True)
#        if os.path.isfile(newFileJ): os.remove(newFileJ)
#        if os.path.isfile(newFileT): os.remove(newFileT)

        
    try:
        if msg['text'] != '':
            command = msg['text']
            print('Got command: ' + command)
    except:
        print("No text in this message")
        

    if command == '/time':
        sendMessage(chat_id, str(datetime.datetime.now()))
    elif '/adduser' in command:
        if len(command.split(' ')) > 1:
            usrname = command.split(' ')[1]
        else:
            usrname = ""
        if usrname == "" :
            usrname = str(sender)
        adduser(usrname)
        sendMessage(chat_id, "User "+usrname+" added")
    elif '/deluser' in command:
        if len(command.split(' ')) > 1:
            usrname = command.split(' ')[1]
        else:
            usrname = ""
        if usrname == "" :
            usrname = str(sender)
        deluser(usrname)
        sendMessage(chat_id, "User "+usrname+" deleted")
    elif command == '/help':
        sendMessage(chat_id, "/adduser /deluser /time /exit")
    elif command == '/exit':
        global active
        active = False
        sendMessage(chat_id, "The bot will shutdown in 10 seconds")
    elif command != '':
        tr_cmd = Zorba.translate(command)
        if "SAYHELLO" == tr_cmd:
            res = "  ^_^\n"
            res = res + "(*.*)\n"
            res = res + "  ---"
            sendMessage(chat_id, res)
        elif "WHAT?" == tr_cmd:
            answer = chatter.reply(command)
            sendMessage(chat_id, str(answer), voice)
        else:
            print(tr_cmd)
            #sendMessage(chat_id, str(tr_cmd))
            cmdoutput = ""
            cmdoutput = subprocess.check_output(tr_cmd, shell=True).decode('UTF-8')
            print("OUTPUT:" + cmdoutput)
            
            if cmdoutput != "":
                if cmdoutput[:8] == "photo://":
                    tmpfile = cmdoutput.replace("photo://", "")
                    tmpfile = tmpfile.replace("\n", "")
                    if os.path.isfile(tmpfile):
                        bot.sendPhoto(chat_id, open(tmpfile, "rb"), caption = tmpfile)
                        os.remove(tmpfile)
                elif cmdoutput[:4] == "Msg:":
                    msg = cmdoutput.replace("Msg:", "")
                    msg = msg.encode().decode('unicode_escape')
                    if msg != '':
                        sendMessage(chat_id, str(msg), voice)
            else:
                sendMessage(chat_id, str(tr_cmd))


#TODO: rewrite this function to send user text written by other scripts on a temporary file (that gets removed after sending message)
#https://www.michaelcho.me/article/using-pythons-watchdog-to-monitor-changes-to-a-directory
#def my_callback(pin):
#    input_value = 0 #GPIO.input(pin)
#    print("The GPIO pin input "+str(pin)+" has value: "+str(input_value))
#    users = listusers()
#    if users != "":
#        for usr in users:
#            sendMessage(usr, "The button on GPIO pin "+str(pin)+" changed value: "+str(input_value))



bot.message_loop(handle)
print('I am listening ...')

while active:
    time.sleep(10)
print("Exiting")
sys.exit()
