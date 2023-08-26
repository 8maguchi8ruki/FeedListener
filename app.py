from crypt import methods
from xml.etree.ElementTree import tostring
from gtts import gTTS
from bs4 import BeautifulSoup as bs4
import requests
import time
from flask import request
from flask import render_template,jsonify
from flask import Flask , session
import contact_me
import re
import random
import os
import shutil
from flask import Flask, render_template, url_for, redirect
import time
import requests
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = os.urandom(12)
print(app.secret_key)
oauth = OAuth(app)

##### ホーム #####
@app.route('/', methods=['GET','POST'])
def index():
    return render_template("index.html")

##### ヘルプページ #####
@app.route('/help/', methods=['GET','POST'])
def help():
    return render_template("help.html")
##### プライバシポリシーページ #####
@app.route('/policy/', methods=['GET','POST'])
def policy():
    return render_template("policy.html")
##### お問い合わせページ #####
@app.route('/contact/', methods=['GET','POST'])
def contact():
    return render_template("contact.html")
##### お問い合わせ成功ページ #####
@app.route('/contact-success/', methods=['GET','POST'])
def contact_success():
    name = request.form.get('name')
    email = request.form.get('email')
    text = request.form.get('textarea')
    print(name,email,text)
    contact_me.send(name,email,text)
    return render_template("contact-success.html")


##### 検索ページ #####
@app.route('/search', methods=['GET','POST'])
def search():
    sitename = request.form.get('sitename')
    print(sitename)
    return render_template("search.html",sitename = sitename)



##### 検索結果ページ #####
class TITLE:
    title = ""
@app.route('/result', methods=['GET','POST'])
def result():
    if not os.path.exists("static/files/audio"):
        print("audioフォルダを作成しました")
        os.mkdir("static/files/audio")
    # HTMLformから値を取得
    url = request.form.get('url')
    path = "static/files/text/article.txt"
    sitename = ""
    target_site = ""
    def Scraping(class_name , sitename):
        #記事を取得しarticle.txtへ書き込み  
        res = requests.get(url)
        soup = bs4(res.content, "lxml")
        title = soup.find("title").text
        i = 0
        print(class_name)
            
        text_array = []
        for tag in soup.select(class_name):
            text = str(tag.text)
            print(text)
            print(sitename)
            text_array.append(text)

            # 日本語記事の場合のみ英文を排除対象とする
            if not "EN" in target_site or "EN" in sitename:
                # 文の開始が連続した英単語で始まり、文の終わりが英単語の場合 ('は固有名詞などに対応するため 例:Tom's)
                text = re.sub(r"\n(\w|')+\s+(\w|')+\s.*(\w|')+\n" , "" , text)
            # 文にリンクが含まれている場合
            text = re.sub(r"https?://.+\n" , "" , text)
            # 改行されていないが、文にリンクが含まれている場合
            text = re.sub(r"https?://.+.html" , "" , text)
            text = re.sub(r"https?://.+/" , "" , text)

            # 出力データの確認
            print("ここから下は削除済みデータです")
            print(text)

            if i == 0:
                f = open(path, 'w', encoding="UTF-8")
                f.write(text)
                f.close()
            else:
                f = open(path, 'a', encoding="UTF-8")   
                f.write(text)
                f.close()
            i = i + 1
        print(text_array)
        
            
    ##### サイト識別 #####
    # Cnet
    if "japan.cnet.com" in url:
        sitename = "cnet"
        Scraping(".article_body p" , sitename)
    # Techcrunch
    elif "techcrunch.com" in url:
        sitename = "techcrunch"
        Scraping(".article-content p" , sitename)
    #GIZMODO
    elif "gizmodo.jp" in url:
        sitename = "gizmodo"
        Scraping(".p-post-content p" , sitename)
    # 産経新聞
    elif "sankei.com" in url:
        sitename = "sankei"
        Scraping(".article-body p" , sitename)
    # NHK
    elif "nhk.or.jp" in url:
        sitename = "nhk"
        Scraping(".body-text" , sitename)
    # Yahoo!
    elif "news.yahoo.co.jp" in url:
        sitename = "yahoo"
        Scraping(".article_body p" , sitename)
    # CNN
    elif "cnn.co.jp" in url:
        sitename = "cnn"
        Scraping("#leaf-body p" , sitename)
    # CNN -EN
    elif "edition.cnn.com" in url:
        sitename = "cnn -EN"
        Scraping(".zn-body__paragraph" , sitename)
    elif "gigazine.net" in url:
        sitename = "GIGAZINE"
        Scraping("#article .cntimage .preface" , sitename)
    

    ##### 最新の投稿 #####
    elif url == "new-post":
            target_site = request.form.get('target-site')
            print(target_site)
            # Cnet
            if target_site == "Cnet":
                res = requests.get("https://japan.cnet.com/release/")
                soup = bs4(res.content, "lxml")
                a = soup.find('a', class_="bold")
                url = a.get('href')
                url = "https://japan.cnet.com/" + url
                Scraping(".article_body p" , target_site)
            # GIZMODO【テクノロジ】
            elif target_site == "GIZMODO【テクノロジ】":
                res = requests.get("https://www.gizmodo.jp/category/technology/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【サイエンス】
            elif target_site == "GIZMODO【サイエンス】":
                res = requests.get("https://www.gizmodo.jp/category/science/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【プロダクト】
            elif target_site == "GIZMODO【プロダクト】":
                res = requests.get("https://www.gizmodo.jp/category/product/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【エンタメ】
            elif target_site == "GIZMODO【エンタメ】":
                res = requests.get("https://www.gizmodo.jp/category/entertainment/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【ライフ】
            elif target_site == "GIZMODO【ライフ】":
                res = requests.get("https://www.gizmodo.jp/category/lifestyle/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【デザイン】
            elif target_site == "GIZMODO【デザイン】":
                res = requests.get("https://www.gizmodo.jp/category/design/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【ビジネス】
            elif target_site == "GIZMODO【ビジネス】":
                res = requests.get("https://www.gizmodo.jp/category/business/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【ニュース】
            elif target_site == "GIZMODO【ニュース】":
                res = requests.get("https://www.gizmodo.jp/category/news/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            

            # 産経新聞【社会】
            elif target_site == "産経新聞【社会】":
                res = requests.get("https://www.sankei.com/affairs/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # 産経新聞【政治】
            elif target_site == "産経新聞【政治】":
                res = requests.get("https://www.sankei.com/politics/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # 産経新聞【国際】
            elif target_site == "産経新聞【国際】":
                res = requests.get("https://www.sankei.com/world/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # 産経新聞【経済】
            elif target_site == "産経新聞【経済】":
                res = requests.get("https://www.sankei.com/economy/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # 産経新聞【スポーツ】
            elif target_site == "産経新聞【スポーツ】":
                res = requests.get("https://www.sankei.com/sports/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # 産経新聞【エンタメ】
            elif target_site == "産経新聞【エンタメ】":
                res = requests.get("https://www.sankei.com/entertainments/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)

            
            # CNN【国際】
            elif target_site == "CNN【国際】":
                res = requests.get("https://www.cnn.co.jp/world/")
                soup = bs4(res.content, "lxml")
                ul = soup.find('ul', class_="list-news-line")
                li = ul.find('li')
                a = li.find('a')
                url = a.get('href')
                url = "https://www.cnn.co.jp/" + url
                print(url)
                Scraping("#leaf-body p" , target_site)
            # CNN【アメリカ】
            elif target_site == "CNN【アメリカ】":
                res = requests.get("https://www.cnn.co.jp/usa/")
                soup = bs4(res.content, "lxml")
                ul = soup.find('ul', class_="list-news-line")
                li = ul.find('li')
                a = li.find('a')
                url = a.get('href')
                url = "https://www.cnn.co.jp/" + url
                print(url)
                Scraping("#leaf-body p" , target_site)
            # CNN【ビジネス】
            elif target_site == "CNN【ビジネス】":
                res = requests.get("https://www.cnn.co.jp/business/")
                soup = bs4(res.content, "lxml")
                ul = soup.find('ul', class_="list-news-line")
                li = ul.find('li')
                a = li.find('a')
                url = a.get('href')
                url = "https://www.cnn.co.jp/" + url
                print(url)
                Scraping("#leaf-body p" , target_site)
            # CNN【テクノロジ】
            elif target_site == "CNN【テクノロジ】":
                res = requests.get("https://www.cnn.co.jp/tech/")
                soup = bs4(res.content, "lxml")
                ul = soup.find('ul', class_="list-news-line")
                li = ul.find('li')
                a = li.find('a')
                url = a.get('href')
                url = "https://www.cnn.co.jp/" + url
                print(url)
                Scraping("#leaf-body p" , target_site)
            # CNN【エンタメ】
            elif target_site == "CNN【エンタメ】":
                res = requests.get("https://www.cnn.co.jp/showbiz/")
                soup = bs4(res.content, "lxml")
                ul = soup.find('ul', class_="list-news-line")
                a = ul.find('a')
                url = a.get('href')
                url = "https://www.cnn.co.jp/" + url
                print(url)
                Scraping("#leaf-body p" , target_site)


            # GIGAZINE【アプリ】
            elif target_site == "GIGAZINE【アプリ】":
                res = requests.get("https://gigazine.net/news/C37/")
                soup = bs4(res.content, "lxml")
                div = soup.find('div', class_="thumb")
                a = div.find('a')
                url = a.get('href')
                print(url)
                Scraping("#article .cntimage .preface" , target_site)
            # GIGAZINE【サービス】
            elif target_site == "GIGAZINE【サービス】":
                res = requests.get("https://gigazine.net/news/C5/")
                soup = bs4(res.content, "lxml")
                div = soup.find('div', class_="thumb")
                a = div.find('a')
                url = a.get('href')
                print(url)
                Scraping("#article .cntimage .preface" , target_site)
            # GIGAZINE【サイエンス】
            elif target_site == "GIGAZINE【サイエンス】":
                res = requests.get("https://gigazine.net/news/C29/")
                soup = bs4(res.content, "lxml")
                div = soup.find('div', class_="thumb")
                a = div.find('a')
                url = a.get('href')
                print(url)
                Scraping("#article .cntimage .preface" , target_site)   
            # GIGAZINE【ゲーム】
            elif target_site == "GIGAZINE【ゲーム】":
                res = requests.get("https://gigazine.net/news/C10/")
                soup = bs4(res.content, "lxml")
                div = soup.find('div', class_="thumb")
                a = div.find('a')
                url = a.get('href')
                print(url)
                Scraping("#article .cntimage .preface" , target_site)
            # GIGAZINE【映画】
            elif target_site == "GIGAZINE【映画】":
                res = requests.get("https://gigazine.net/news/C23/")
                soup = bs4(res.content, "lxml")
                div = soup.find('div', class_="thumb")
                a = div.find('a')
                url = a.get('href')
                print(url)
                Scraping("#article .cntimage .preface" , target_site) 
            # GIGAZINE【アニメ】
            elif target_site == "GIGAZINE【アニメ】":
                res = requests.get("https://gigazine.net/news/C20/")
                soup = bs4(res.content, "lxml")
                div = soup.find('div', class_="thumb")
                a = div.find('a')
                url = a.get('href')
                print(url)
                Scraping("#article .cntimage .preface" , target_site) 
            # GIGAZINE【生物】
            elif target_site == "GIGAZINE【生物】":
                res = requests.get("https://gigazine.net/news/C33/")
                soup = bs4(res.content, "lxml")
                div = soup.find('div', class_="thumb")
                a = div.find('a')
                url = a.get('href')
                print(url)
                Scraping("#article .cntimage .preface" , target_site)
            # GIGAZINE【レビュー】
            elif target_site == "GIGAZINE【レビュー】":
                res = requests.get("https://gigazine.net/news/C12/")
                soup = bs4(res.content, "lxml")
                div = soup.find('div', class_="thumb")
                a = div.find('a')
                url = a.get('href')
                print(url)
                Scraping("#article .cntimage .preface" , target_site)
            

            # TechCrunch【AI】-EN
            elif target_site == "TechCrunch【AI】-EN":
                res = requests.get("https://techcrunch.com/category/artificial-intelligence/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="post-block__title")
                a = h2.find('a')
                url = a.get('href')
                print(url)
                Scraping(".article-content p" , target_site)
            # TechCrunch【Crypto】-EN
            elif target_site == "TechCrunch【Crypto】-EN":
                res = requests.get("https://techcrunch.com/category/cryptocurrency/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="post-block__title")
                a = h2.find('a')
                url = a.get('href')
                print(url)
                Scraping(".article-content p" , target_site)
            # TechCrunch【Startups】-EN
            elif target_site == "TechCrunch【Startups】-EN":
                res = requests.get("https://techcrunch.com/category/startups/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="post-block__title")
                a = h2.find('a')
                url = a.get('href')
                print(url)
                Scraping(".article-content p" , target_site)
    else:
        return render_template("404.html")


    #article.txtをarticle.mp3へ変換
    print("----- 記事情報取得中 -----")
    time.sleep(2)
    f = open(path, 'r',encoding="UTF-8")
    print("----- 音声ファイル作成中 -----")
    data = f.read()
    if "EN" in target_site or "EN" in sitename:
        hoge = gTTS(data,lang="en")
    else:
        hoge = gTTS(data,lang="ja")
    rannum = random.uniform(0,10000)    
    hoge.save(f"static/files/audio/article.mp3")
    f.close()

    def get_title(t):
        res = requests.get(url)
        soup = bs4(res.content , "lxml")
        t.title = soup.find("title").text
    t = TITLE()

    get_title(t)

    # 最新の履歴データのIDを取得
    return render_template('result.html', result=data, url = url , title = t.title , rannum = rannum)



if __name__ == "__main__":
    app.run()


