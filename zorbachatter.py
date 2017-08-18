#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Run this code with python3
#


from chatterbot import ChatBot

class ZorbaChatter(object):
    
    def __init__(self, lang = "en-US"):
        self.language = lang
        self.chatbot = ChatBot(
            'Ron Obvious',
            trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
        )
    def train(self):
        # Train based on the english corpus
        self.chatbot.train("chatterbot.corpus.english.greetings")
    
    def reply(self, phrase = ""):
        # Get a response to an input statement
        response = self.chatbot.get_response(phrase)
        #response = chatbot.get_response("Hello, how are you today?")

        return response

