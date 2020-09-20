import aipi.chatbot
import aipi.asr
import aipi.tts
import eyepi.eyespi

import logging
from multiprocessing import Value, Process, Manager, Queue
import time
from ctypes import c_char_p
import signal
import sys

def signal_handler(sig, frame):
    # print a status message
    print("[INFO] You pressed `ctrl + c`! Exiting...")
    sys.exit()

def eye_process():
    signal.signal(signal.SIGINT, signal_handler)

    eye = eyepi.eyespi.r2d2Eye()
    eye.start()

def tts_process(response):
    signal.signal(signal.SIGINT, signal_handler)

    tts = aipi.tts.r2d2Tts(engine='polly')
    
    while 1:
        tts.speak(response.get())

def asr_process(in_text):
    signal.signal(signal.SIGINT, signal_handler)

    asr = aipi.asr.r2d2Asr(ambient=False)
    
    while 1:
        in_text.put(asr.get_asr())

def chatbot_process(in_text, response):
    signal.signal(signal.SIGINT, signal_handler)

    chatbot = aipi.chatbot.r2d2Bot(dbpath='db.sqlite3',read_only=True)
    
    while 1:
        response.put(chatbot.get_response(in_text.get()))

def voice_process(response):
    signal.signal(signal.SIGINT, signal_handler)

    tts = aipi.tts.r2d2Tts(engine='polly')
    tts.speak("준비 시작")

    chatbot = aipi.chatbot.r2d2Bot(dbpath='db.sqlite3',read_only=True)
    #chatbot = aipi.chatbot.r2d2Bot(corpus='aipi/data/corpus/chichat.json', dbpath='db.sqlite3',read_only=False)
    #chatbot = aipi.chatbot.r2d2Bot(corpus='aipi/data/corpus/kibots_corpus.json', dbpath='db.sqlite3',read_only=False)
    asr = aipi.asr.r2d2Asr(ambient=True)
    
    chatbot.get_response("안녕하세요")
    tts.speak("준비 완료")

    while 1:
        asrout = asr.get_asr()
        if asrout=="ERROR": continue
        output = chatbot.get_response(asrout)
        response.put(output)
        print("chatbot output:"+output)
        tts.speak(output)

def process_manager():
    
    in_text = Queue()
    response = Queue()

    voice_processor = Process(target=voice_process,
                                args=(response,))
    eye_processor = Process(target=eye_process,
                                args=())

    #voice_processor.start()
    eye_processor.start()

    #voice_processor.join()
    eye_processor.join()


if __name__ == "__main__":
    process_manager()
 

