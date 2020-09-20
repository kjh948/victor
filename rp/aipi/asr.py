# -*- coding: utf-8 -*-
'''import sys
from importlib import reload
reload(sys)
sys.setdefaultencoding('utf-8')
'''

import os
import subprocess  # needed to run external program raspistill
import time
from os import path
import sys

import speech_recognition as sr
import signal


EXEC_PATH = path.join(path.dirname(path.realpath(__file__)))

class r2d2Asr(object):

    def __init__(self, lang='ko-KR', ambient=False):
        self.r = sr.Recognizer()
        self.lang = lang
        self.WAV_FILE = path.join(path.dirname(path.realpath(__file__)), "out.wav")
        self.ambient = ambient
        if ambient:
            self.source = sr.Microphone()
            with self.source as source:
                self.r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
                print("Audio Calibration was done!")

    def get_asr(self):
        if not self.ambient:
            #VAD using adinrec
            #note: threshold for adinrec needs to be readjusted for a new HW setting
            try:
                subprocess.check_call(EXEC_PATH+'/adinrec -lv 1000 -zc 200 '+ self.WAV_FILE, shell=True,stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                print( "Ping stdout output:\n", e.output)
                return 'ERROR'
            with sr.WavFile(self.WAV_FILE) as source:
                audio = self.r.record(source)  # read the entire WAV file
            try:
                str = self.r.recognize_google(audio, language=self.lang)
                print(str)
            except:
                str = 'ERROR'
                print( "can't understand")
            #os.remove(self.WAVE_FILE)
        else:
            try:
                with self.source as source:
                    audio = self.r.listen(source)
                    str=self.r.recognize_google(audio,language = self.lang)
            except:
                str = 'error'

        return str
def signal_handler(signal, frame):
    sys.exit(0)

if __name__ == "__main__":
    asr = r2d2Asr(ambient=False)
    signal.signal(signal.SIGINT, signal_handler)

    while 1:
        out = asr.get_asr()
        print("you said: "+out)
 
