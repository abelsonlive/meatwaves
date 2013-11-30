from socketIO_client import SocketIO
import re
from twython import Twython
import os
import base64
from PIL import Image
import StringIO
import subprocess
from random import choice
import requests
import yaml
import json
import requests
import bitly_api

# Listening to meatspac, sending back to staging for now
# This can be just an ADDRESS variable when/if listening to meatspac and posting back
PRODUCTION = 'https://chat.meatspac.es'
STAGING = 'http://chat-staging.meatspac.es'

MT = re.compile("^MT(:)?", re.IGNORECASE)
NUMBERS = range(0, 1000000)

CONFIG = yaml.safe_load(open('meatwaves.yml'))

class MeatWaves(object):

    def __init__(self, address):
      
      # ashley's app
      self.app_url = 'http://localhost:9393/'

      # twitter
      self.consumer_key = CONFIG["consumer_key"]
      self.consumer_secret = CONFIG["consumer_secret"]
      self.access_token = CONFIG["access_token"]
      self.access_token_secret = CONFIG["access_token_secret"]
      self.api = self.connect_to_twitter()

      # bitly
      self.bitly_access_token = CONFIG['bitly_access_token']

      self.bitly = self.connect_to_bitly()

      # socket
      print "Listening to %s" % address
      with SocketIO(address) as socketIO:
          socketIO.on('message', self.on_message)
          socketIO.wait()


    def connect_to_twitter(self):
      api = Twython(
        self.consumer_key,
        self.consumer_secret,
        self.access_token,
        self.access_token_secret
        )
      return api

    def connect_to_bitly(self):
      api = bitly_api.Connection(access_token = self.bitly_access_token)
      return api

    def shorten_url(self, url):
      return self.bitly.shorten(uri=str(url))['url']

    def format_media(self, b64):
      # format string
      b64 = b64.split('base64,')[1]

      # pad string
      b64 += "=" * ((4 - len(b64) % 4) % 4)

      # decode string
      data = base64.b64decode(b64)

      # read in encoded data
      f = StringIO.StringIO(data)

      # open image
      im = Image.open(f)

      # save image and open it up again, don't know why i have to do this, it's a hack...
      path = 'img%s.gif' % str(choice(NUMBERS))
      im.save(path)
      media = open(path, 'rb')

      # remove image
      subprocess.call(['rm', path])

      return media


    def post_tweet(self, message, key):
      message = MT.sub('', message).strip()
        
      # disable direct messages
      if message.lower().startswith('d '):
        message = message[1:].strip()

      # shorten url
      long_url = "%smeats/%s.gif" % (self.app_url, key)
      short_url = self.shorten_url(long_url)
      print short_url
      status = "%s\r\n%s" % (message, short_url)

      # post
      self.api.update_status(status=status)     


    def on_message(self, *args):
      try:            
        # Grab the message.
        message_data = args[0]
        
        # unnest data
        data = dict(
          message = message_data['chat']['value']['message'].strip(),
          gif = message_data['chat']['value']['media'],
          fingerprint = message_data['chat']['value']['fingerprint'],
          created = int(message_data['chat']['value']['created']),
          key = message_data['chat']['key']
        )
        
        print data['message']
        
        # post it to ruby app
        r = requests.post(self.app_url + "meats/new/", data=data)

        # tweet it
        m = MT.search(data['message'])
        if m: 
          self.post_tweet(data['message'], data['key'])

      except Exception as e:
        print e

if __name__ == '__main__':
    mw = MeatWaves(PRODUCTION)


