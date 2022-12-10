#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
import logging
import time
import tweepy
import configparser

BUTTON_GPIO = 5
logging.basicConfig(filename='lazy.log', format='%(asctime)s %(message)s', level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_secret = config['twitter']['api_secret']
access_token = config['twitter']['access_token']
access_secret = config['twitter']['access_secret']

#authentication
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

#status = api.PostUpdate('Hello World!')
#print(status)

def signal_handler(sig, frame):
    GPIO.cleanup()
    logging.info('Program Exit')
    sys.exit(0)

def button_pressed_callback(channel):
    tweet = "Hello Twitter! " + time.strftime("%a, %d %b %Y %I:%M:%S ", time.localtime())
    logging.info('Button Pressed')
    print("Sending Tweet: ", tweet)
    api.update_status(status=tweet)
    #also log time to file and save

if __name__ == '__main__':
    
    logging.info('Lazy.py program started')

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=100)
    
    logging.info('Init complete. Waiting for input')
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
