from slackbot.bot import Bot
from slacker import Slacker
import slackbot_settings
from scrape import scrape_active, scrape_upcoming, strtotime_date
import datetime

'''
    金土の夜６時に動くようにする
'''

def make_message(channel,slack,s,message):
    '''
    引数にいくつ出力か指定しても良いかも
    '''
    message += "\n"
    for i in s:
        message += "\n".join(i)
        message += "\n"
    slack.chat.post_message(channel, message, as_user=True)

#チャンネルのアプリを追加できているかの確認
def info(channel,slack):
    active_contests = scrape_active()
    upcoming_contests = scrape_upcoming()
    if len(active_contests)!= 0:
        make_message(channel,slack,active_contests,"*[開催中のコンテスト一覧]*")
    else:
        slack.chat.post_message(channel,"*開催中のコンテストはありません*",as_user=True)
    if len(upcoming_contests)!= 0:
        make_message(channel,slack,upcoming_contests,"*[今週のコンテスト一覧]*")
    else:
        slack.chat.post_message(channel,"*今週のコンテストはありません*",as_user=True)

def anounce_contest_today(today, slack, channel):
    scheduled_contests = scrape_upcoming()
    for contest in scheduled_contests:
        contest_date = strtotime_date(contest[1].split("(")[0]).date()
        if today == contest_date:
            message = "【告知】\n今日のコンテスト\n"
            message += "\n".join(contest)
            print(message)
            slack.chat.post_message(channel, message, as_user=True)

def anounce_contest_before_day(today, slack, channel):
    scheduled_contests = scrape_upcoming()
    for contest in scheduled_contests:
        contest_date = strtotime_date(contest[1].split("(")[0]).date()
        if today + datetime.timedelta(days=1) == contest_date:
            message = "【告知】\n明日のコンテスト\n"
            message += "\n".join(contest)
            slack.chat.post_message(channel, message, as_user=True)

def main():
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
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()