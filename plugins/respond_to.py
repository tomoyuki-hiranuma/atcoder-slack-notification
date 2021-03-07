import sys
from slackbot.bot import respond_to
sys.path.append('..')
from scrape import scrape_upcoming
import numpy as np


@respond_to("予定")
def when_is_contest(message):
  upcoming_contests = scrape_upcoming()
  for line in upcoming_contests:
    text = "\n"
    text += "\n".join(line)
    message.reply(text)