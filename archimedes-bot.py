#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Run this code with python3.5
#

#-ocr image from telegram photo https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#fetch-images-sent-to-your-bot
#updates = bot.get_updates()
#>>> print([u.message.photo for u in updates if u.message.photo])
#bot.send_voice(chat_id=chat_id, voice=open('tests/telegram.ogg', 'rb'))
#http://telepot.readthedocs.io/en/latest/reference.html


import time
import random
import datetime
import telepot
import os
import sys
import subprocess
from zorbacmd import ZorbaCMD
from speechrecognition import ZorbaSR
from zorbachatter import ZorbaChatter

telegramtoken = '' #telegram bot token from BotFather
checkuserid = 1 #enable users whitelist, so only certain people can talk with this bot
usersfile = 'botusers.csv' #the file where we store the list of users who can talk with bot
attemptsfile = '/tmp/attempts.log' #the file where we log denied accesses
active = 1 #if set to 0 the bot will stop

language = "it-IT"

Zorba = ZorbaCMD(language)

chatter = ZorbaChatter(language)
#chatter.clearTraining()
chatter.train()

if telegramtoken == '' and os.path.isfile("telegramtoken.txt"):
    text_file = open("telegramtoken.txt", "r")
    telegramtoken = text_file.read().replace("\n", "")
    text_file.close()

print("Connecting to Telegram...")
bot = telepot.Bot(telegramtoken)
print(bot.getMe())



    
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
            bot.sendMessage(chat_id, "I don't talk with strangers, dear "+str(sender))
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
    
    try:
        if msg['voice'] != '':
            file_id = msg['voice']['file_id']
            tmpdate = '/tmp/' + str(datetime.datetime.now()).replace(" ","_").replace(":","_") + '.jpeg'
            #tmpdate = tmpfile.replace(" ","_")
            #tmpdate = tmpfile.replace(":","_")
            newFileO = "/tmp/voice" + tmpfile + "_" + str(sender) + ".ogg"
            newFileW = "/tmp/voice" + tmpfile + "_" + str(sender) + ".wav"
            if os.path.isfile(newFileO): os.remove(newFileO)
            if os.path.isfile(newFileW): os.remove(newFileW)
            bot.download_file(file_id, newFileO)
            #http://telepot.readthedocs.io/en/latest/reference.html
            os.system("ffmpeg -i " + newFileO + " -acodec pcm_s16le -ac 1 -ar 16000 "+ newFileW)
            sr = ZorbaSR(language, newFileW)
            command = sr.recognize()
            print("Recognized " + command)
            bot.sendMessage(chat_id, "YOU: " + command)
            if os.path.isfile(newFileO): os.remove(newFileO)
            if os.path.isfile(newFileW): os.remove(newFileW)
    except:
        print("No voice in this message")
        
        
    try:
        if msg['text'] != '':
            command = msg['text']
            print('Got command: ' + command)
    except:
        print("No text in this message")
        

    if command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif '/adduser' in command:
        if len(command.split(' ')) > 1:
            usrname = command.split(' ')[1]
        else:
            usrname = ""
        if usrname == "" :
            usrname = str(sender)
        adduser(usrname)
        bot.sendMessage(chat_id, "User "+usrname+" added")
    elif '/deluser' in command:
        if len(command.split(' ')) > 1:
            usrname = command.split(' ')[1]
        else:
            usrname = ""
        if usrname == "" :
            usrname = str(sender)
        deluser(usrname)
        bot.sendMessage(chat_id, "User "+usrname+" deleted")
    elif command == '/help':
        bot.sendMessage(chat_id, "/adduser /deluser /time /exit")
    elif command == '/exit':
        global active
        active = False
        bot.sendMessage(chat_id, "The bot will shutdown in 10 seconds")
    elif command != '':
        tr_cmd = Zorba.translate(command)
        if "SAYHELLO" == tr_cmd:
            res = "  ^_^\n"
            res = res + "(*.*)\n"
            res = res + "  ---"
            bot.sendMessage(chat_id, res)
        elif "WHAT?" == tr_cmd:
            answer = chatter.reply(command)
            bot.sendMessage(chat_id, str(answer))
        else:
            print(tr_cmd)
            #bot.sendMessage(chat_id, str(tr_cmd))
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
                    bot.sendMessage(chat_id, str(msg))
            else:
                bot.sendMessage(chat_id, str(tr_cmd))


#TODO: rewrite this function to send user text written by other scripts on a temporary file (that gets removed after sending message)
#def my_callback(pin):
#    input_value = 0 #GPIO.input(pin)
#    print("The GPIO pin input "+str(pin)+" has value: "+str(input_value))
#    users = listusers()
#    if users != "":
#        for usr in users:
#            bot.sendMessage(usr, "The button on GPIO pin "+str(pin)+" changed value: "+str(input_value))



bot.message_loop(handle)
print('I am listening ...')

while active:
    time.sleep(10)
print("Exiting")
sys.exit()
