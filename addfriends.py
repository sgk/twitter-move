#!/usr/bin/env python

import twitter
import time
import sqlite3
import sys

api = twitter.Api(
  consumer_key='XXXXXXXXXXXXXXXXXXXXXXXXX',
  consumer_secret='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
  access_token_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
  access_token_secret='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
)

def sleep():
  d = 60
  while d > 0:
    sys.stderr.write('Sleeping %d... \r' % d)
    time.sleep(1)
    d -= 1

def addfavs():
  db = sqlite3.connect('twitter.db')
  db.execute('''
    create table if not exists
    friends(
      id integer primary key,
      done integer default 0
    )
  ''')

  for id in db.execute('select id from friends where done = 0'):
    id = id[0]
    print id

    while True:
      try:
        api.CreateFriendship(user_id=id, follow=False)
        break
      except twitter.TwitterError as e:
        if isinstance(e.message, dict):
          sleep()
          continue
        code = e.message[0]['code']
        if code == 88:
          sleep()
          continue
        raise e
    db.execute('update friends set done = 1 where id = ?', (id,))
    db.commit()
  print 'Done'

if __name__ == '__main__':
  try:
    addfavs()
  except KeyboardInterrupt:
    pass
