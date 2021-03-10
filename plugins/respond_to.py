import sys
from slackbot.bot import respond_to
sys.path.append('..')
from run import info
import slackbot_settings
import numpy as np


@respond_to("いつ")
def when_is_contest(message):
  slack = Slacker(slackbot_settings.API_TOKEN)
  info(slackbot_settings.CHANNEL, slack)