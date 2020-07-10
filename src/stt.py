#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import time

import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

def listen():
    with sr.Microphone() as source:
      print("Say something!")
      audio = r.listen(source)
      print('understanding')
# recognize speech using Sphinx
    try:
        rec = r.recognize_sphinx(audio)
        print('$:' + rec)
        return rec
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        return ''
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
        return ''
