#!/usr/bin/env python

import twitter
import time
import sqlite3

api = twitter.Api(
  consumer_key='XXXXXXXXXXXXXXXXXXXXXXXXX',
  consumer_secret='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
  access_token_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
  access_token_secret='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
)

def getfriends():
  db = sqlite3.connect('twitter.db')
  db.execute('''
    create table if not exists
    friends(
      id integer primary key,
      done integer default 0
    )
  ''')

  for id in api.GetFriendIDs():
    print id
    db.execute('insert or ignore into friends(id) values(?)', (id,))
  db.commit()
  print 'Done'

if __name__ == '__main__':
  try:
    getfriends()
  except KeyboardInterrupt:
    pass
