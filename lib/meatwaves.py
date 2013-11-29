from socketIO_client import SocketIO
import re
from twython import Twython
import os
import base64
from PIL import Image
import StringIO
import subprocess
from random import choice
import yaml
import dataset
import json

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
      self.app_endpoint = 'http://localhost:9393/meats/new/'

      # twitter
      self.consumer_key = CONFIG["consumer_key"]
      self.consumer_secret = CONFIG["consumer_secret"]
      self.access_token = CONFIG["access_token"]
      self.access_token_secret = CONFIG["access_token_secret"]
      self.api = self.connect_to_twitter()

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


    def post_tweet(self, message, gif):
      message = MT.sub('', message).strip()
      
      # disable direct messages
      if message.lower().startswith('d '):
        message = message[1:].strip()

      print message

      # format media
      media = self.format_media(gif)

      # post
      self.api.update_status_with_media(status=message, media=media)     


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
        
        # post it to ruby app
        r = requests.post(self.app_endpoint, data=data)

        print data["message"]
        # tweet it
        m = MT.search(data['message'])
        if m:
          self.post_tweet(data['message'], data['gif'])

      except:
        pass

if __name__ == '__main__':
    mw = MeatWaves(PRODUCTION)


