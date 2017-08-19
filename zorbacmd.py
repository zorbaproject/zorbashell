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
#try:
#    import gnureadline as readline
#except ImportError:
    import readline
#from __future__ import braces #this makes it possible to use {} instead of indentation

#readline.parse_and_bind('tab: complete')
#readline.parse_and_bind('set editing-mode vi')

class ZorbaCMD(object):

    def __init__(self, lang = "en-US"):
        self.language = lang
        #self.language = "it-IT"

#        self.continuous = True
        self.dict_configured = False
        self.mydict = []


    def translate( usrphrase ):
        phrase = usrphrase.lower()
        mycmd = ""
        #global dict_configured
        #global self.mydict
    
        if self.dict_configured == False:
            #loading dictionary
            dict_file = os.path.abspath(os.path.dirname(sys.argv[0])) + "/lang/" + language + "/dict.csv"
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
                elif "noun-zorba" in self.mydict[2][ni]:
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
                    nouns.append(self.mydict[3][ni])
                    #TODO: we should enable multiple meanings for nouns, using couplewith, for example: /usr/bin/firefox | firefox;open | stop; so you get the first when coupled with open and the second when cuopled with stop. This could be useful in a few cases
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
            #print(nouns)
            #print(verbs)
    

    
        if mycmd == "":
            mycmd = "WHAT?" #we didn't get anything, that's weird
        return mycmd;
        

    
    #def runcmd( tr_cmd ):
    #    if "SET continuous FALSE" == tr_cmd:
    #        global continuous
    #        continuous = False
    #    elif "SAYHELLO" == tr_cmd:
    #        print(" ^_^")
    #        print("(*.*)")
    #        print(" ---")
    #    elif "WHAT?" == tr_cmd:
    #        print("???")
    #    else:
    #        print(tr_cmd)
    #        #os.system(tr_cmd)
    



#    for (i, item) in enumerate(sys.argv):
#        if item == "-h":
#            print("Options:\n -l specify language\n -p specify phrase to analize\n -c continuous mode, works as a shell")
#            
#        if item == "-l":
#            language = sys.argv[i+1]
#            print("LANGUAGE: " + language)
#            
#        if item == "-p":
#            #TODO: we should split phrases here like we do in the -c case
#            tr_cmd = translate(sys.argv[i+1])
#            runcmd(tr_cmd)
#            
#        if item == "-c":
#            while continuous:
#                phrase = input("You: ")
#                phrases = list(filter(None, re.split("[;.!?]", phrase))) #if we've got multiple phrases, we split them
#                for (p, itemp) in enumerate(phrases):
#                    tr_cmd = translate(phrases[p])
#                    runcmd(tr_cmd)
    
