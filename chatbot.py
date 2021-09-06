import praw
import time
import random
import datetime

# 在这配置Reddit验证所需的信息
config = {
    "user_agent": "Kalftazhi GA v0.1",
    "client_id": "待设置",
    "client_secret": "待设置",
    "username": "待设置",
    "password": "待设置",
}

title = "Kalftazhi高雅创作"
target_username = "u/Kalftazhi"
target_subreddit = "CLTV"

# 每两分钟查询Reddit状态并回复
poll_internal = 120

def GetRecentComments(user, start_time):
  return [c for c in user.comments.new(limit=20)
          if  c.subreddit.display_name == 'CLTV'
          and c.created > start_time
          and c.created > time.time() - 3600 * 24]

def LoadKalftazhiDissertation(title):
  with open('kalftazhi.txt') as f:
    return [title + "：" + l.strip() for l in f.readlines()]

kalftazhi = LoadKalftazhiDissertation(title)

reddit = praw.Reddit(
    user_agent = config["user_agent"],
    client_id = config["client_id"],
    client_secret = config["client_secret"],
    username = config["username"],
    password = config["password"],
);

subreddit = reddit.subreddit(target_subreddit)

def ReplyOneRound():
  # Look at all comments within 4 hours from now
  start_time = time.time() - 3600 * 4
  
  user = next(reddit.redditors.search(target_username))
  user_comments = GetRecentComments(user, start_time)
  
  me = reddit.user.me()
  my_comments = GetRecentComments(me, start_time)
  
  # Find all comments to reply
  my_replied_ids = set([c.parent().id for c in my_comments])
  to_reply = [c for c in user_comments if c.id not in my_replied_ids]
  
  print("To reply: ", to_reply)
  
  for r in to_reply:
    body = random.choice(kalftazhi)
    r.reply(body)

while True:
  print("Time:", datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
  ReplyOneRound()
  time.sleep(poll_internal)
