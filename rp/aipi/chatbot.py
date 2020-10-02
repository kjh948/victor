# -*- coding: utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
from chatterbot import ChatBot
import logging
from chatterbot.response_selection import get_random_response

from chatterbot.trainers import ChatterBotCorpusTrainer


class r2d2Bot(object):

    def __init__(self, dbpath=None, corpus = None,read_only=True):
        #open db file here
        #try:
            if corpus is None:
                self.bot_engine = ChatBot(
                    'R2D2',
                    storage_adapter="chatterbot.storage.SQLStorageAdapter",
                    logic_adapters=[
                        {
                            'statement_comparison_function': "chatterbot.statement_comparison_function.levenshtein_distance",
                            "response_selection_method": "chatterbot.response_selection.get_random_response",
                            'default_response': '냠냠냠',
                            'import_path': 'chatterbot.logic.BestMatch',
                            'maximum_similarity_threshold': 0.20
                        }
                    ],
                    database=dbpath,
                    read_only = read_only,
                    response_selection_method=get_random_response,
                )
                print('chatbot DB loaded successfully')
            else:
                self.bot_engine = ChatBot(
                    'R2D2',
                    storage_adapter="chatterbot.storage.SQLStorageAdapter",
                    logic_adapters=[
                        {
                            'import_path': 'chatterbot.logic.BestMatch',
                            'default_response': '냠냠냠',
                            'maximum_similarity_threshold': 0.20
                        }
                    ],
                    database=dbpath,
                    read_only=read_only
                )
                trainer = ChatterBotCorpusTrainer(self.bot_engine)

                trainer.train(corpus)

                #self.bot_engine.train(["How are you?","I am good.","That is good to hear.","Thank you", "You are welcome.",] )


                #self.bot_engine.trainer.export_for_training('./json.json')
                print('chatbot corpus loaded successfully')
        #except:
            #print('Error with DB loading')
    def get_response(self, query):
        response = self.bot_engine.get_response(query)
        print("Bot: " + response.text)
        if response.confidence<0.2: return "냠냠냠"
        else: return response.text


if __name__ == "__main__":
    #bot = r2d2Bot(corpus="/usr/local/lib/python2.7/dist-packages/chatterbot_corpus/data/english/ai.yml")

    #bot = r2d2Bot(corpus="./kibots_corpus.json")
    #bot = r2d2Bot(corpus="./test.yml")
    #bot = r2d2Bot(dbpath='db.sqlite3',corpus='./data/corpus/chichat.json',read_only=False)
    bot = r2d2Bot(dbpath='db.sqlite3',read_only=False)

    #bot = r2d2Bot()
    while True:
        query = input("Tell me : ")
        response = bot.get_response(query)
        #print("Bot: " + response.text)
        #print(response)
