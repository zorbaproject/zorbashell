#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Run this code with python2.7
#

#-ocr image from telegram photo https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#fetch-images-sent-to-your-bot
#updates = bot.get_updates()
#>>> print([u.message.photo for u in updates if u.message.photo])
#-voice recognition from telegram voice  https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#download-a-file
#file_id = message.voice.file_id
#>>> newFile = bot.get_file(file_id)
#>>> newFile.download('voice.ogg')
#bot.send_voice(chat_id=chat_id, voice=open('tests/telegram.ogg', 'rb'))
#http://telepot.readthedocs.io/en/latest/reference.html


import time
import random
import datetime
import telepot
import os
import sys
#import RPi.GPIO as GPIO
#from w1thermsensor import W1ThermSensor



telegramtoken = '' #telegram bot token from BotFather
checkuserid = 1 #enable users whitelist, so only certain people can talk with this bot
usersfile = 'botusers.csv' #the file where we store the list of users who can talk with bot
attemptsfile = '/tmp/attempts.log' #the file where we log denied accesses
relay = 18 #GPIO pin where we put the relay or the LED
button = 17 #GPIO pin where we put the button
active = 1 #if set to 0 the bot will stop

if telegramtoken == '' and os.path.isfile("telegramtoken.txt"):
    text_file = open("telegramtoken.txt", "r")
    telegramtoken = text_file.read().replace("\n", "")
    text_file.close()

print "Connecting to Telegram..."
bot = telepot.Bot(telegramtoken)
print bot.getMe()


    
def listusers():
    if not os.path.isfile(usersfile):
        return ''
    text_file = open(usersfile, "r")
    lines = text_file.read().split(',')
    text_file.close()
    del lines[-1] #remove last element since it is blank
    return lines

def adduser(name):
    csv = ""
    users = listusers()
    if users != "":
        for usr in users:
            csv = csv+usr+","
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
    chat_id = msg['chat']['id']
    sender = msg['from']['id']

    users = listusers()


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
    
    try:
        if msg['voice'] != '':
            file_id = msg['voice']['file_id']
            #newFile = bot.getFile(file_id)
            bot.download_file(file_id, 'voice.ogg')
            #http://telepot.readthedocs.io/en/latest/reference.html
    except:
        print "No voice in this message"
        
    command = ''
    try:
        if msg['text'] != '':
            command = msg['text']
            print 'Got command: ' + command
    except:
        print "No text in this message"

    if command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif '/adduser' in command:
        if len(command.split(' ')) > 1:
            usrname = command.split(' ')[1]
            adduser(usrname)
            bot.sendMessage(chat_id, "User "+usrname+" added")
    elif '/deluser' in command:
        if len(command.split(' ')) > 1:
            usrname = command.split(' ')[1]
            deluser(usrname)
            bot.sendMessage(chat_id, "User "+usrname+" deleted")
    #elif 'webcam' in command:
    #    tmpfile = '/tmp/'+str(datetime.datetime.now())+str(sender)+'.jpeg'
    #    tmpfile = tmpfile.replace(" ","_")
    #    tmpfile = tmpfile.replace(":","_")
    #    os.system("streamer -s 1280x720 -f jpeg -o "+tmpfile)
    #    bot.sendPhoto(chat_id, open(tmpfile, "rb"), caption = tmpfile)
    #    os.remove(tmpfile)
    #elif '/pinon' in command:
    #    pin = relay
    #    if len(command.split(' ')) > 1:
    #        pin = command.split(' ')[1]
    #    GPIO.setup(int(pin), GPIO.OUT)
    #    GPIO.output(int(pin), GPIO.HIGH)
    #    bot.sendMessage(chat_id, "Set "+str(pin)+" HIGH")
    #elif '/pinoff' in command:
    #    pin = relay
    #    if len(command.split(' ')) > 1:
    #        pin = command.split(' ')[1]
    #    GPIO.setup(int(pin), GPIO.OUT)
    #    GPIO.output(int(pin), GPIO.LOW)
    #    bot.sendMessage(chat_id, "Set "+str(pin)+" LOW")
    #elif '/temperature' in command:
    #    sensor = W1ThermSensor()
    #    temperature_in_celsius = sensor.get_temperature()
    #    bot.sendMessage(chat_id, "Temperature is "+str(temperature_in_celsius)+"° Celsius")
    elif command == '/help':
        bot.sendMessage(chat_id, "/adduser /deluser /time /exit")
    elif command == '/exit':
        global active
        active = False
        bot.sendMessage(chat_id, "The bot will shutdown in 10 seconds")
    elif command != '':
        bot.sendMessage(chat_id, 'echo: ' + command + ' from: '+str(sender))

def my_callback(pin):
    input_value = 0 #GPIO.input(pin)
    print "The GPIO pin input "+str(pin)+" has value: "+str(input_value)
    users = listusers()
    if users != "":
        for usr in users:
            bot.sendMessage(usr, "The button on GPIO pin "+str(pin)+" changed value: "+str(input_value))


#print "Connecting to Telegram..."
#bot = telepot.Bot(telegramtoken)
#print bot.getMe()

#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

#GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.add_event_detect(button, GPIO.BOTH)
#GPIO.add_event_callback(button, my_callback)

bot.message_loop(handle)
print 'I am listening ...'

while active:
    time.sleep(10)
print "Exiting"
sys.exit()
