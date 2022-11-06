#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
import logging

BUTTON_GPIO = 5
logging.basicConfig(filename='lazy.log', format='%(asctime)s %(message)s', level=logging.INFO)

def signal_handler(sig, frame):
    GPIO.cleanup()
    logging.info('Program Exit')
    sys.exit(0)

def button_pressed_callback(channel):
    print("Button Pressed!")
    logging.info('Button Pressed')
    #also log time to file and save

if __name__ == '__main__':
    
    logging.info('Lazy.py program started')

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=100)
    
    logging.info('Init complete. Waiting for input')
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
