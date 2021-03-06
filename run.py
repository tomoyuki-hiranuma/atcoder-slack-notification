from slackbot.bot import Bot
from slacker import Slacker
import slackbot_settings
import scrape
import datetime

def make_message(channel,slack,s,message):
    '''
    引数にいくつ出力か指定しても良いかも
    '''
    for i in s:
        message=message+"\n"+i[0]+"\n"+i[1]+"\n"
    slack.chat.post_message(channel, message, as_user=True)


    '''
    メッセージを一つにするために変更した
    slack.chat.post_message(channel, message, as_user=True)
    for i in s:
        slack.chat.post_message(channel,i[0],as_user=True,unfurl_links=True)
        slack.chat.post_message(channel,i[1],as_user=True,unfurl_links=True)
        #slack.chat.post_message(channel,i[2],as_user=True,unfurl_links=True)
    '''


#チャンネルのアプリを追加できているかの確認
def info(channel,slack):
    s1=scrape.scrape_active()
    s2=scrape.scrape_upcoming()
    if len(s1)!=0:
        make_message(channel,slack,s1,"*[開催中のコンテスト一覧]*")
    else:
        slack.chat.post_message(channel,"*開催中のコンテストはありません*",as_user=True)
    if len(s2)!=0:
        make_message(channel,slack,s2,"*[今週のコンテスト一覧]*")
    else:
        slack.chat.post_message(channel,"*今週のコンテストはありません*",as_user=True)

def main():
    channel="kyo-pro"
    slack = Slacker(slackbot_settings.API_TOKEN)
    if datetime.datetime.today().weekday()==0:
        info(channel,slack)
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()