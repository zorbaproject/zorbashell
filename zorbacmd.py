#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from os import path
import sys
import shutil
import os
import select
import subprocess
import csv
import re


class ZorbaCMD(object):

    def __init__(self, lang = "en-US"):
        self.language = lang
        #self.language = "it-IT"

#        self.continuous = True
        self.dict_configured = False
        self.mydict = []
        self.telegramusers = []
        
    def set_telegramusers(self, listusers):
        try:
            self.telegramusers = listusers
        except:
            self.telegramusers = []
        
    def find_between(self, s, first, last ):
        try:
            start = 0
            if first != "":
                start = s.index( first ) + len( first )
            end = len(s)-1
            if last != "":
                end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""


    def translate(self, usrphrase):
        phrase = usrphrase.lower()
        mycmd = ""
        #global dict_configured
        #global self.mydict
    
        if self.dict_configured == False:
            #loading dictionary
            dict_file = os.path.abspath(os.path.dirname(sys.argv[0])) + "/lang/" + self.language + "/dict.csv"
            origdict = list(csv.reader(open(dict_file), delimiter=';')) #this is [row][column]
            self.mydict = list(map(list, zip(*origdict))) #this is [colum][row]
            self.dict_configured = True
        
        #replace ,'! and other simbols since they are usually not necessary to understand a simple statement
        phrase = phrase.replace("'", " ") #this mean that "don't" becomes "don t", so the regex should just be "don"
        phrase = phrase.replace(",", "")
        phrase = phrase.replace("!", "")
        phrase = phrase.replace(";", "")
        phrase = phrase.replace(":", "")
        #phrase = phrase.replace("\"", "") # double qotes could be useful, keep them
    
    
        verbID = -1
        nouns = []
        verbs = [] #TODO we could make these two lists global, so it would be possibile to keep track of every verb/noun specified byt he user in the last conversation. So if there is a verb and nothing that matches its couplewith in the current phrase, just look for previous phrases.

    
        #separate words by " " Please note that str.split() without passing any arguments splits by all whitespaces (space, multiple spaces, tab, newlines, etc)
        wordslist = phrase.split()
        for word in wordslist:
            indexes = [t for t,val in enumerate(self.mydict[1]) if re.match(val, word)]
            if len(indexes)>0 and indexes[0]>-1 and "verb" in self.mydict[2][indexes[0]]:
                verbID = indexes[0]
                break #we stop at the first verb, if we have two verbs than we actually have got two prhases from the user and we need to separe them.


        if verbID < 0:
            ni = -1
            for word in wordslist:
                indexes = [t for t,val in enumerate(self.mydict[1]) if re.match(val, word)]
                if len(indexes)>0:
                    ni = indexes[0]
            if ni>-1: 
                if "noun-program" in self.mydict[2][ni]:
                    mycmd = mycmd + self.mydict[3][ni] #it's a program, just run it
                elif "noun-zorba" in self.mydict[2][ni] and len(wordslist)<2:
                    #print("Hi") #are you trying to wake me up from standby?
                    mycmd="SAYHELLO"
                elif "noun-" in self.mydict[2][ni]:
                    couplewith = self.mydict[4][ni].split(" | ") #we got a file or a GPIO port... it means we look for the default verb to couple it
                    ci = 0
                    if len(couplewith)>0:
                        vi = -1
                        indexes = [t for t,val in enumerate(self.mydict[1]) if re.match(val, couplewith[ci])]
                        if len(indexes)>0:
                            vi = indexes[0]
                        if vi>-1 and "verb" in self.mydict[2][vi]:
                            verbID = vi
                            nouns.append(self.mydict[3][ni])

        verbcoupled = 0
                    
        if verbID > 0:
            couplewith = self.mydict[4][verbID].split(" | ")
            ni = -1
            for word in wordslist:
                indexes = [t for t,val in enumerate(self.mydict[1]) if re.match(val, word)]
                if len(indexes)>0:
                    ni = indexes[0]
                    
                if ni>-1 and self.mydict[2][ni] in couplewith:
                    if self.mydict[2][ni] == "context-search":
                        searchverb = ""
                        indexes = [r for r,val in enumerate(wordslist) if re.match(self.mydict[1][verbID], val)]
                        ti = -1
                        if len(indexes)>0:
                            searchverb = wordslist[(indexes[0])]
                        subphrase = self.find_between(usrphrase.lower(), searchverb, word) #all chars between verb and wiki
                        subphrase = self.stripuseless(subphrase)
                        subphrase = self.unifyspaces(subphrase)
                        if subphrase == "" or subphrase == " ":
                            for tmpword in wordslist:
                                if tmpword.lower() != searchverb and tmpword.lower() != word:
                                    subphrase = subphrase + " " + tmpword
                        nouns.append(subphrase)
                        verbcoupled = couplewith.index(self.mydict[2][ni])
                        verbs.append(self.mydict[3][verbID].split(" | ")[verbcoupled])
                    else:
                        nouns.append(self.mydict[3][ni])
                        verbcoupled = couplewith.index(self.mydict[2][ni])
                        verbs.append(self.mydict[3][verbID].split(" | ")[verbcoupled])

            if "*" in couplewith:
                indexes = [r for r,val in enumerate(wordslist) if re.match(self.mydict[1][verbID], val)]
                ti = -1
                if len(indexes)>0:
                    ti = indexes[0]
                while (ti+1)<len(wordslist):
                    nouns.append(wordslist[ti+1]) #TODO: we should ignore articles, so if we get "the" or "a" we just jump to the following word
                    ti = ti +1
                verbcoupled = couplewith.index("*")
                verbs.append(self.mydict[3][verbID].split(" | ")[verbcoupled])
    

            
            ni = 0
            nni = 0
            while nni<len(nouns):
                if nouns[nni]!="zorba":
                    ni=nni #we ignore the word "zorba" if there are other alternatives
                    break
                nni = nni + 1
            
            
            if ni<len(verbs):
                mycmd = mycmd + verbs[ni].replace("$1", nouns[ni])
                mycmd = mycmd.replace("$L", self.language)
            
             #   mycmd = mycmd.replace("  ", " ")
                
                
            #now we strip useless words
            mycmd = mycmd.replace("./scripts/", os.path.abspath(os.path.dirname(sys.argv[0]))+"/scripts/")
            mycmd = self.stripuseless(mycmd)
            mycmd = self.unifyspaces(mycmd)
            #print(nouns)
            #print(verbs)
    

    
        if mycmd == "":
            mycmd = "WHAT?" #we didn't get anything, that's weird
        return mycmd;
        
        
    
    def stripuseless(self, phrase):
        for i in range(len(self.mydict[2])):
            if self.mydict[2][i] == "useless":
                phrase = re.sub(self.mydict[1][i], "", phrase)
        return phrase
    
    def unifyspaces(self, phrase):
        while "  " in phrase:
            phrase = phrase.replace("  ", " ")
        phrase = re.sub("\A ", "", phrase)
        phrase = re.sub(" \Z", "", phrase)
        return phrase
    
    def sendMessage(self, chat_id, bot, answer = "", voice = False, photofile = ""):
        #global bot
        #global language
        try:
            bot.getMe()
            botvalid = True
        except:
            botvalid = False
        print(photofile)
        if answer != "":
            if voice == True:
                #we should send audio
                newFileW = speech.speak(str(answer), str(chat_id))
                if chat_id != "" and botvalid == True:
                    bot.sendVoice(chat_id, open(newFileW, "rb"), caption = str(answer))
                else:
                    os.system('aplay "' + newFileW + '"')
                    if os.path.isfile(newFileW): os.remove(newFileW)
            else:
                if chat_id != "" and botvalid == True:
                    bot.sendMessage(chat_id, str(answer))
                else:
                    print(str(answer))
        if photofile != "":
            if chat_id != "" and botvalid == True:
                bot.sendPhoto(chat_id, open(photofile, "rb"), caption = photofile)
            else:
                print(photofile)
                os.system('w3m "' + photofile +'"')
            os.remove(photofile)
        
    
    def display_output(self, cmdoutput, chat_id, bot, voice = False):
        chat_ids = []
        if chat_id == "":
            try:
                users = self.telegramusers
                if users != "":
                    for usr in users:
                        chat_ids.append(usr)
            except:
                chat_ids.append(chat_id)
        else:
            chat_ids.append(chat_id)
        if cmdoutput == "":
            return ""
        if cmdoutput[:8] == "photo://":
            tmpfile = cmdoutput.replace("photo://", "")
            tmpfile = tmpfile.replace("\n", "")
            if os.path.isfile(tmpfile):
                for cid in chat_ids:
                    self.sendMessage(cid, bot, "", voice, tmpfile)
                if chat_id == "":
                    self.sendMessage(chat_id, bot, "", voice, tmpfile)
        elif cmdoutput[:4] == "Msg:":
            msg = cmdoutput.replace("Msg:", "")
            msg = msg.encode().decode('unicode_escape')
            if str(msg) != '':
                for cid in chat_ids:
                    self.sendMessage(cid, bot, str(msg), voice)
                if chat_id == "":
                    self.sendMessage(chat_id, bot, str(msg), voice)
    
