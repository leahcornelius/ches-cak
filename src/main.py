#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class
from create_chatbot_instance import new_ches_cak
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer
from color import color
from ttb import ttb
from arduino_com import write_to
from arduino_com import wait_for_power
import urllib
from threading import Thread
try:
    from queue import Queue  # Python 3 import
except ImportError:
    from Queue import Queue  # Python 2 import

import speech_recognition as sr
online = 0
def test_online():
    try:
        url = "http://amionline.net/"
        urllib.request.urlopen(url)
        status = "Connected to internet, using online services"
    except:
        status = "Not connected to internet, using local stt"
    print (status)
    if status == "Connected to internet, using online services": online = 1
test_online()
# Create a new chat bot named ches cak
chatbot = new_ches_cak()
debug = True
to_ard = True
if (wait_for_power() == False):
  print("failed to connect to ardunio, wont be printing")
  ttb("ard con failed")
  to_ard = False
else:
  print("Connected to ardino")
  recognize_thread = Thread(target=ttb, args=('hello',))
  recognize_thread.daemon = True
  recognize_thread.start()
r = sr.Recognizer()
audio_queue = Queue()
with sr.Microphone() as source:
    print('please do not speak')
    write_to('Do not speak now')
    r.adjust_for_ambient_noise(source)
    print('ready')

def recognize_worker():
    # this runs in a background thread
    while True:
        audio = audio_queue.get()  # retrieve the next audio processing job from the main thread
        if audio is None: break  # stop processing if the main thread is done

        # received audio data, now we'll recognize it using Google Speech Recognition
        if online == 1:
            try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
                read = r.recognize_google(audio)
            except sr.UnknownValueError:
                read = ''
            except sr.RequestError as e:
                print(e)
                read = ''
            

            audio_queue.task_done()  # mark the audio processing job as completed in the queue
        else:
            try:
                read = r.recognize_sphinx(audio)
            except sr.UnknownValueError:
                print("Sphinx could not understand audio")
                read = ''
            except sr.RequestError as e:
                print("Sphinx error; {0}".format(e))
                read = ''
            if read != '':
              response = chatbot.get_response(read)
              print('response: ', response.text)
              if debug == True:
                print('read: ', read)
                a = color.GREEN if response.confidence > 0.4 else color.RED
                print(color.BLUE, 'Confidence: ', response.confidence, a, 'Would say: ', response.confidence > 0.4, color.END)
                if a = color.GREEN:
                    recognize_thread = Thread(target=ttb, args=(response.text,))
                    recognize_thread.daemon = True
                    recognize_thread.start()
    
                    if (to_ard == True):
                        write_to("w" + read)
                        write_to(response.text)
            

# start a new thread to recognize audio, while this thread focuses on listening
recognize_thread = Thread(target=recognize_worker)
recognize_thread.daemon = True
recognize_thread.start()
with sr.Microphone() as source:
    try:
        while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
            audio_queue.put(r.listen(source))
            print('pushed to queue')
    except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        pass
audio_queue.join()  # block until all current audio processing jobs are done
audio_queue.put(None)  # tell the recognize_thread to stop
recognize_thread.join()  # wait for the recognize_thread to actually stop
