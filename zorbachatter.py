#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Run this code with python3
#

#Instead of using chatterbot, we should store conversations in bag-of-words form for the question and plain text for the answer. When we get a phrase from the user, we look for the most similar bag-of-words in the archive and reply with the plain text answer.

import os
import os.path
import sys

from chatterbot import ChatBot

class ZorbaChatter(object):
    
    def __init__(self, lang = "english"):
        self.language = lang
        self.chatbot = ChatBot(
            'Zorba',
            logic_adapters=[
            "chatterbot.logic.MathematicalEvaluation",
            "chatterbot.logic.TimeLogicAdapter",
            "chatterbot.logic.BestMatch"
            ],
            trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
        )
        self.instdir = "/usr/local/lib/python3.5/dist-packages/chatterbot_corpus/data/" + self.language + "/"
        self.localdir = os.path.abspath(os.path.dirname(sys.argv[0])) + "/lang/" + self.language + "/chatbotcorpus/"
        self.database = os.path.abspath(os.path.dirname(sys.argv[0])) + "/db.sqlite3"
        
    def train(self):
        if self.checkdirnotempty(self.localdir):
            print(self.localdir)
            self.chatbot.train(
                self.localdir
            )
        elif self.checkdirnotempty(self.instdir):
            print(self.instdir)
            self.chatbot.train(
                self.instdir
            )
        else:
            print("Using standard english corpus")
            self.chatbot.train("chatterbot.corpus.english.greetings")
    
    def reply(self, phrase = ""):
        # Get a response to an input statement
        response = self.chatbot.get_response(phrase)
        return response
    
    def clearTraining(self):
        if os.path.isfile(self.database): os.remove(self.database)
    
    def checkdirnotempty(self, folder = ""):
        check = False
        if os.path.isdir(folder):
            entities = os.listdir(folder)
            for entity in entities:
                if os.path.isfile(folder + entity):
                    check = True
                    break
        return check

