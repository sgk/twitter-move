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

def getfavs():
  db = sqlite3.connect('twitter.db')
  db.execute('''
    create table if not exists
    favs(
      id integer primary key,
      done integer default 0
    )
  ''')

  max_id = 0
  while True:
    try:
      favs = api.GetFavorites(count=200, max_id=max_id)
    except twitter.TwitterError as e:
      if e.message[0]['code'] != 88:
        raise e
      print 'Sleeping 10...'
      time.sleep(10)
      continue
    if len(favs) == 0:
      break

    for f in favs:
      print f.id
      db.execute('insert or ignore into favs(id) values(?)', (f.id,))
    db.commit()
    max_id = favs[-1].id - 1
    time.sleep(3)
  print 'Done'

if __name__ == '__main__':
  try:
    getfavs()
  except KeyboardInterrupt:
    pass
