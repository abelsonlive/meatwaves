from socketIO_client import SocketIO
import re
import requests
from twython import Twython
import os
import base64
from PIL import Image
import StringIO
import subprocess
from random import choice
import yaml

# Listening to meatspac, sending back to staging for now
# This can be just an ADDRESS variable when/if listening to meatspac and posting back
ADDRESS = 'https://chat.meatspac.es'
ADDRESS2 = 'http://chat-staging.meatspac.es'

M2T = re.compile("^MT(:)?")
NUMBERS = range(0, 1000000)

CONFIG = yaml.safe_load(open('meatwaves.yml'))

class MeatWaves(object):

    def __init__(self):
      self.consumer_key = CONFIG["consumer_key"]
      self.consumer_secret = CONFIG["consumer_secret"]
      self.access_token = CONFIG["access_token"]
      self.access_token_secret = CONFIG["access_token_secret"]

      self.api = self.connect_to_twitter()

      print CONFIG["consumer_key"]
      print CONFIG["consumer_secret"]
      print CONFIG["access_token"]
      print CONFIG["access_token_secret"]
      
      print "Listening to %s" % ADDRESS2
      with SocketIO(ADDRESS2) as socketIO:
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

    def on_message(self, *args):
      try:            
        # Grab the message. Meatspac messages are nested dicts in the form:
        all_message_data = args[0]
        message = all_message_data['chat']['value']['message'].strip()
        b64 = all_message_data['chat']['value']['media']

        m = M2T.search(message)
        if m:
          message = M2T.sub('', message).strip()
          
          # disable direct messages
          if message.lower().startswith('d'):
            message = message[1:].strip()

          print message

          # format media
          media = self.format_media(b64)

          # post
          self.api.update_status_with_media(status=message, media=media)

      except Exception as e:
        print(e.message)

if __name__ == '__main__':
    mw = MeatWaves()


