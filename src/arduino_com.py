#!/usr/bin/env python3
import serial
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
def wait_for_power():
#    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if (line == "online"):
              return True
def write_to(txt):
    ser.write(txt.encode('utf-8') + "\n".encode('utf-8'))
'''
if (wait_for_power()):
  print("connected")
else:
  print("watiing")

write_to("hello, tester")
'''
