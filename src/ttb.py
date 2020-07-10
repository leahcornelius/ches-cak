#from playsound import playsound
import time
import sys
from color import color
import os

num = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
ligatures = ['ae', 'sh', 'hh', 'oo', 'ck', 'th', 'ph']
test_out = False
log = False
def delete_last_line():
    "Use this function to delete the last line in the STDOUT"

    #cursor up one line
    sys.stdout.write('\x1b[1A')

    #delete last line
    sys.stdout.write('\x1b[2K')

def ttb(text):
  print("Saying: ", text)
  i = 0
  for elem in text:
    
    i += 1
    #delete_last_line()
    if log:
      if log:
        print("On char: ", i, "of ", len(text), "chars")
    if elem != " ":
      if elem.isalpha() == True:
        os.system ("aplay " + '~/ches cak/sounds/ttb/' + elem.lower() + '.wav > /dev/null 2>&1')
        #os.system ("aplay " + '../sounds/ttb/' + elem.lower() + '.wav')
      else:
        if elem == ",":
          time.sleep(0.25)
        elif elem.isnumeric() == True:
          for as_text in num[int(elem)]:
              os.system ("aplay " + '~/ches cak/sounds/ttb/' + as_text + '.wav > /dev/null 2>&1')
        else:
            time.sleep(0.5)
    else:
      if log:
        print("elem =  ")
      time.sleep(0.15)
if test_out:
  while True:
    ttb(input("$:"))
