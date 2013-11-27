from socketIO_client import SocketIO
import re
import requests
import tweepy


# Listening to meatspac, sending back to staging for now
# This can be just an ADDRESS variable when/if listening to meatspac and posting back
ADDRESS = 'https://chat.meatspac.es'
ADDRESS2 = 'http://chat-staging.meatspac.es'

M2T = re.compile("^MT(:)?")

class MeatWaves(object):

    def __init__(self):
        self.consumer_key = 'PcKs75IuujSnsaeBeD1ieA'
        self.consumer_secret = 'TSi7RGypeSZkYVVVuaXrEkVZcxuR3wvmsxF4FGgBo'
        self.access_token = '2215261214-FVPClsoHnlxfmq1CKHlYCI0lFsEJjBHSMvDtUkt'
        self.access_token_secret = 'efUCTN8xCxnEX3Zm3u1wHM1d4KeEVAIoHjW5pqxrnhufT'

        self.api = self.connect_to_twitter()

        print "Listening to %s" % ADDRESS
        with SocketIO(ADDRESS) as socketIO:
            socketIO.on('message', self.on_message)
            socketIO.wait()

    def connect_to_twitter(self):
      auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
      auth.set_access_token(self.access_token, self.access_token_secret)
      return tweepy.API(auth)

    def on_message(self, *args):
        try:            
            # Grab the message. Meatspac messages are nested dicts in the form:
            # {u'chat': {u'value': {u'media': u'data:image/gif;base64,<wow    so base64   such image>', u'message': '<witicism here>', u'ttl': 600000, u'created': 1385499795344, u'fingerprint': u'93d944673197120b6d611d3014d81949'}, u'key': u'1385499795344!f72be0da-83d7-4bff-8c6e-562928ae6162'}}
            all_message_data = args[0]
            message = all_message_data['chat']['value']['message'].strip()

            m = M2T.search(message)
            if m:
              print message
              message = M2T.sub('', message).strip()
              try:
                self.api.update_status(message)
              except tweepy.TweepError:
                pass
        except:
          pass

if __name__ == '__main__':
    mw = MeatWaves()


