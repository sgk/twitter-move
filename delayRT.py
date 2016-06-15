#!/usr/bin/env python3

import twitter
import time
import sqlite3

# old account
api = twitter.Api(
  consumer_key='XXXXXXXXXXXXXXXXXXXXXXXXX',
  consumer_secret='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
  access_token_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
  access_token_secret='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
)


def main():
  db = sqlite3.connect('twitter.db')
  db.execute('''
    create table if not exists
    settings(
      key string primary key,
      value string
    )
  ''')
  cur = db.execute('select value from settings where key = ?', ['lastRT'])
  row = cur.fetchone()
  lastid = int(row[0]) if row else 0

  posts = api.GetUserTimeline(screen_name='ssci', count=100, since_id=lastid, exclude_replies=True)
  posts.reverse()
  for post in posts:
    if lastid < post.id:
      lastid = post.id
    print(post.id, post.text)
    try:
      api.PostRetweet(post.id)
    except twitter.TwitterError:
      pass
    time.sleep(10)

  db.execute('insert or replace into settings values (?, ?)', ['lastRT', str(lastid)])
  db.commit()

if __name__ == '__main__':
  main()
