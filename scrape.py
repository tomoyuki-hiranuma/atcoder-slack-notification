from urllib import request
from bs4 import BeautifulSoup
import re
import datetime

#時刻とコンテスト名とURLの組を返す
def scrape_active():
    re_contests = []
    url = "https://atcoder.jp"
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    contests_all = soup.find("div", id="contest-table-active")

    if contests_all is None:
        return re_contests

    contests_tbody_tag = contests_all.find("tbody")
    upcoming_contests = contests_tbody_tag.find_all("tr")
    #コンテスト情報をre_contestsに格納
    # ['title', 'start_date', 'end_date', 'url']
    for c in upcoming_contests:
        re_contests_sub = []
        #コンテストページのurlを取ってurl2に格納
        d = c.find("a",href=re.compile("contests"))
        url2 = url+d.get("href")
        html2 = request.urlopen(url2)
        soup2 = BeautifulSoup(html2, "html.parser")

        title = soup2.find("h1", class_="text-center")
        re_contests_sub.append(title.text)

        sftime = soup2.find_all("time", class_="fixtime-full")
        re_contests_sub.append(sftime[0].text.split("+")[0] + " 開始")
        re_contests_sub.append(sftime[1].text.split("+")[0] + " 終了")

        re_contests_sub.append(url2)

        re_contests.append(re_contests_sub)
    return re_contests

# ['title', 'start_date', 'end_date', 'url']
# 明日コンテストがあれば呼ばれる
def scrape_upcoming():
    re_contests = []
    url = "https://atcoder.jp"
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    contests_all=soup.find("div", id="contest-table-upcoming")

    if contests_all is None:
        return re_contests

    contests_tbody_tag = contests_all.find("tbody")
    upcoming_contests = contests_tbody_tag.find_all("tr")
    #その週にコンテストあるかどうかの判定のために今日の日時を取得
    w=datetime.datetime.today()
    #コンテスト情報をre_contestsに格納
    #コンテストのurlと終了の日時のみ
    for c in upcoming_contests:
        re_contests_sub = []
        d1 = c.find("time")
        #分まで入ってるところだけをスライスして渡す
        #秒などの余計な情報が入っているので
        t = strtotime(d1.text[:16])
        #月曜日に実行を行うのでその週の日曜までにないコンテストは格納しなくて良い
        if (t - w).days >= 7:
            break
        #formatを統一するためにtimetostr関数を使う
        re_contests_sub.append(timetostr(t) + " 開始")
        d2 = c.find("a",href=re.compile("contests"))
        #コンテストページのurlもre_contests_subに格納
        re_contests_sub.append(url + d2.get("href"))
        re_contests.append(re_contests_sub)
    return re_contests

def strtotime(date_sub):
    '''
    datetimeオブジェクトにして返す
    '''
    return datetime.datetime.strptime(date_sub, '%Y-%m-%d %H:%M')

def timetostr(date_sub):
    '''
    datetimeオブジェクトをstrオブジェクトにして返す
    '''
    W = ["月","火","水","木","金","土","日"]
    return ('%d-%d-%d(%s) %d:%s'%(
        date_sub.year, date_sub.month, date_sub.day, W[date_sub.weekday()], date_sub.hour, str(date_sub.minute).ljust(2, "0")
    ))

# print(scrape_active())
# print(scrape_upcoming())