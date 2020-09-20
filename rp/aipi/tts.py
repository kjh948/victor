# -*- coding: utf-8 -*-
import sys
#sys.setdefaultencoding('utf-8')
from gtts import gTTS
from pygame import mixer
import time
import pyttsx3
import subprocess
from boto3 import client

class r2d2Tts(object):
    def __init__(self, lang='ko', engine='google'):
        self.lang = lang
        if engine is 'google':
            #use offline engine
            self.isGoogle = True
            self.isAmazon = False
        elif engine is 'polly':
            self.isGoogle = False
            self.isAmazon = True
            self.polly = client("polly", region_name="ap-northeast-2")
        else: 
            self.isGoogle = False
            self.isAmazon = False
            self.offline_engine = pyttsx3.init()

    def speak(self,utt, isBlock=True):
        if self.isGoogle:
            tts = gTTS(text=utt, lang=self.lang)
            tts.save('response.mp3')
            '''mixer.init()
            mixer.music.load('response.mp3')
            mixer.music.play()
            if isBlock==True:
                while mixer.music.get_busy():
                   time.sleep(1)'''
            #cmdln = 'play response.mp3 overdrive 10 echo 0.8 0.8 5 0.7 echo 0.8 0.7 6 0.7 echo 0.8 0.7 10 0.7 echo 0.8 0.7 12 0.7 echo 0.8 0.88 12 0.7 echo 0.8 0.88 30 0.7 echo 0.6 0.6 60 0.7 gain 8'
            cmdln = 'play response.mp3'# chorus 0.4 0.8 20 0.5 0.10 2 -t echo 0.9 0.8 33 0.9 echo 0.7 0.7 10 0.2 echo 0.9 0.2 55 0.5 gain 25 speed 1.3'
            subprocess.check_call([cmdln], shell=True)
        elif self.isAmazon:
            response = self.polly.synthesize_speech(Text=utt, OutputFormat="mp3", VoiceId="Seoyeon")
            stream = response.get("AudioStream")
            with open('response.mp3', 'wb') as f:
                data = stream.read()
                f.write(data)
            cmdln = 'play response.mp3'# chorus 0.4 0.8 20 0.5 0.10 2 -t echo 0.9 0.8 33 0.9 echo 0.7 0.7 10 0.2 echo 0.9 0.2 55 0.5 gain 25 speed 1.3'
            subprocess.check_call([cmdln], shell=True)

        else:
            try:
                cmdln = 'espeak '
                cmdln = cmdln + '"' + utt + '"'

                cmdln = 'espeak '+ '--stdout "' + utt + '" | play - chorus 0.4 0.8 20 0.5 0.10 2 -t echo 0.9 0.8 33 0.9 echo 0.7 0.7 10 0.2 echo 0.9 0.2 55 0.5 gain 20 speed 1.2'
                # call external program ro take a picture
                subprocess.check_call([cmdln], shell=True)
                #espeak --stdout -s120 -k18 -a200 -v female5 | play -t wav - chorus 0.4 0.8 20 0.5 0.10 2 -t echo 0.9 0.8 33 0.9 echo 0.7 0.7 10 0.2 echo 0.9 0.2 55 0.5 gain 10
            except:
                print( "Ping stdout output:\n")

    def soundPlay(self,fname, isBlock=True):
        mixer.init()
        mixer.music.load(fname)
        mixer.music.play()
        if isBlock==True:
            while mixer.music.get_busy():
                time.sleep(1)
        
    #self.offline_engine = pyttsx.init()
            #self.offline_engine.say(utt)
            #self.offline_engine.runAndWait()
