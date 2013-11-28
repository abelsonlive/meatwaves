from socketIO_client import SocketIO
import re
import requests
from twython import Twython
import os
import base64
from PIL import Image
import StringIO
import subprocess

# Listening to meatspac, sending back to staging for now
# This can be just an ADDRESS variable when/if listening to meatspac and posting back
ADDRESS = 'https://chat.meatspac.es'
ADDRESS2 = 'http://chat-staging.meatspac.es'

M2T = re.compile("^MT(:)?")

class MeatWaves(object):

    def __init__(self):
      self.consumer_key = os.getenv('MT_CONSUMER_KEY')
      self.consumer_secret = os.getenv('MT_CONSUMER_SECRET')
      self.access_token = os.getenv('MT_ACCESS_TOKEN')
      self.access_token_secret = os.getenv('MT_ACCESS_TOKEN_SECRET')

      self.api = self.connect_to_twitter()

      print "Listening to %s" % ADDRESS
      with SocketIO(ADDRESS) as socketIO:
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

      # get original height and width
      im = Image.open(f)

      # save image and open it up again, don't know why i have to do this, it's a hack...
      im.save('img.gif')
      media = open('img.gif', 'rb')

      # remove image
      subprocess.call(['rm', 'img.gif'])

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
          print message
          media = self.format_media(b64)
          try:
            self.api.update_status_with_media(status=message, media=media)
          except tweepy.TweepError:
            pass
      except:
        pass

if __name__ == '__main__':
    mw = MeatWaves()


