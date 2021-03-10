import sys
from slackbot.bot import respond_to
from slacker import Slacker
import numpy as np
import random
import datetime
from pytz import timezone
sys.path.append('..')
from run import info
import slackbot_settings

def select_question():
  random.seed(datetime.datetime.now(timezone('Asia/Tokyo')).day)
  #スクレイピングで最大値取得
  max_contest_number = 194
  contest = random.randint(1, max_contest_number + 1)
  tasks = ['a', 'b', 'c', 'd']
  number = random.choice(tasks)
  url = "https://atcoder.jp/contests/abc{}/tasks/abc{}_{}".format(contest, contest, number)
  return url


@respond_to("いつ")
def when_is_contest(message):
  slack = Slacker(slackbot_settings.API_TOKEN)
  info(slackbot_settings.CHANNEL, slack)

@respond_to("問")
def post_today_question(message):
  slack = Slacker(slackbot_settings.API_TOKEN)
  message = "【今日の1問】\n"
  message += select_question() + "\n"
  slack.chat.post_message(slackbot_settings.CHANNEL, message, as_user=True)
