from slacker import Slacker
import slackbot_settings
import datetime
from run import anounce_contest_before_day, anounce_contest_today


if __name__ == "__main__":
  '''
      TODO
      指定した時間の時に動く
      メッセージ飛ばすと特定のメソッドが動くようにする
  '''
  channel = slackbot_settings.CHANNEL
  slack = Slacker(slackbot_settings.API_TOKEN)
  '''
      金土日のみ動く
  '''
  DATE = ["月","火","水","木","金","土","日"]
  check_date = ["金", "土", "日"]
  if DATE[datetime.datetime.today().weekday()] in check_date:
    anounce_contest_today(datetime.datetime.today(), slack, channel)
    anounce_contest_before_day(datetime.datetime.today(), slack, channel)