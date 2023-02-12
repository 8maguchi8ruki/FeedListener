from crypt import methods
import json
from xml.etree.ElementTree import tostring
from gtts import gTTS
from bs4 import BeautifulSoup as bs4
import requests
import time
from flask import request
from flask import render_template,jsonify
from flask import Flask
import database
import contact_me
import re
import random
import os
import shutil
from lxml import html
 
app = Flask(__name__)
rannum = ""
##### トップページ #####
@app.route('/')
def index():
    if os.path.exists("static/files/audio"):
        print("audioフォルダを削除しました")
        shutil.rmtree("static/files/audio")

    return render_template('index.html')

##### トップページ全サイト取得ajax #####
@app.route('/ajax/all-site/')
def all_site():
    return jsonify(database.select_all_site())

# トップページサイト追加ajax
@app.route('/ajax/add-site/<sitename>')
def add_site(sitename):
    database.update_site(sitename)
    return jsonify(database.select_site())

# トップページサイト削除ajax
@app.route('/ajax/delete-site/<sitename>')
def delete_site(sitename):
    database.delete_site(sitename)
    return jsonify(database.select_site())

##### マイリストページ #####
@app.route('/mylist/', methods=['GET','POST'])
def mylist():
    database.create_all_site()
    return render_template("mylist.html", my_sites = database.select_site())

##### 検索ページ #####
@app.route('/search/', methods=['GET','POST'])
def search():
    sitename = request.form.get('sitename')
    return render_template("search.html",sitename = sitename)

##### 最新の投稿ページ #####
@app.route('/recent/', methods=['GET','POST'])
def recent():
    database.create_all_site()
    return render_template("recent.html", my_sites = database.select_site())

##### セレクトページ #####
@app.route('/select/', methods=['GET','POST'])
def select():
    database.create_all_site() 
    return render_template("select.html", my_sites = database.select_site())

##### ダウンロードページ #####
@app.route('/download/', methods=['GET','POST'])
def download():
    return render_template("download.html")

##### その他ページ #####
@app.route('/others/', methods=['GET','POST'])
def others():
    return render_template("others.html")

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

##### 履歴ページ #####
@app.route('/history/')
def history():
    datas = database.select()
    return render_template('history.html',datas = datas)

##### 履歴全削除ajax #####
@app.route('/ajax/delete-historys/', methods=['GET'])
def ajax_delete_historys():
    return jsonify(database.delete_historys())

##### アーカイブページ #####
@app.route('/archive/',methods=['GET'])
def archive():
    archives = database.archive_sl()
    return render_template('archive.html',archives = archives)

##### アーカイブ登録ajax #####
@app.route('/ajax/<articleID>', methods=['GET'])
def ajax(articleID):
    print(articleID)
    return jsonify(database.archive_up(articleID))

##### アーカイブ全削除ajax #####
@app.route('/ajax/delete-archives/', methods=['GET'])
def ajax_delete_archives():
    return jsonify(database.delete_archives())

##### アーカイブ個別削除ajax #####
@app.route('/ajax/delete/<articleID>', methods=['GET'])
def ajax_delete(articleID):
    return jsonify(database.delete_this(articleID))

##### 検索結果ページ #####
class TITLE:
    title = ""
@app.route('/result/', methods=['GET','POST'])
def result():
    if not os.path.exists("static/files/audio"):
        print("audioフォルダを作成しました")
        os.mkdir("static/files/audio")

    # HTMLformから値を取得
    url = request.form.get('url')
    print(url)
    path = "static/files/text/article.txt"
    sitename = ""
    target_site = ""
    def Scraping(class_name , sitename):
        #記事を取得しarticle.txtへ書き込み  
        res = requests.get(url)
        soup = bs4(res.content, "lxml")
        title = soup.find("title").text
        print(title)
        print(url)
        # 新しい履歴を反映
        database.update(title,url)
        i = 0
        print(class_name)
        for tag in soup.select(class_name):
            text = str(tag.text)
            print(text)
            # GIGAZINE記事のパースプログラム
            if sitename == "gigazine":
                print(text)
                re.sub('http://', '', text)
                print("ここから下が削除済み")
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

    ##### サイト識別 #####
    # Cnet
    if "japan.cnet.com" in url:
        sitename = "cnet"
        Scraping(".article_body p" , sitename)
    # Techcrunch
    # elif "jp.techcrunch.com" in url:
    #     sitename = "techcrunch"
    #     Scraping(".article-entry.text p" , sitename)
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
    # ITmedia
    # elif "itmedia.co.jp" in url:
    #     sitename = "itmedia"
    #     Scraping(".inner p" , sitename)
    # GIGAZINE
    # elif "gigazine.net" in url:
    #     sitename = "gigazine"
    #     Scraping(".preface" , sitename)
    
    # 最新の投稿
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
            # GIZMODO【 テクノロジ 】
            elif target_site == "GIZMODO【 テクノロジ 】":
                res = requests.get("https://www.gizmodo.jp/category/technology/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【 サイエンス 】
            elif target_site == "GIZMODO【 サイエンス 】":
                res = requests.get("https://www.gizmodo.jp/category/science/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【 プロダクト 】
            elif target_site == "GIZMODO【 プロダクト 】":
                res = requests.get("https://www.gizmodo.jp/category/product/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【 エンタメ 】
            elif target_site == "GIZMODO【 エンタメ 】":
                res = requests.get("https://www.gizmodo.jp/category/entertainment/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【 ライフ 】
            elif target_site == "GIZMODO【 ライフ 】":
                res = requests.get("https://www.gizmodo.jp/category/lifestyle/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【 デザイン 】
            elif target_site == "GIZMODO【 デザイン 】":
                res = requests.get("https://www.gizmodo.jp/category/design/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【 ビジネス 】
            elif target_site == "GIZMODO【 ビジネス 】":
                res = requests.get("https://www.gizmodo.jp/category/business/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # GIZMODO【 ニュース 】
            elif target_site == "GIZMODO【 ニュース 】":
                res = requests.get("https://www.gizmodo.jp/category/news/")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="p-archive-cardTitle")
                a = h3.find('a')
                url = a.get('href')
                url = "https://www.gizmodo.jp/" + url
                Scraping(".p-post-content p" , target_site)
            # 産経新聞【 速報 】
            elif target_site == "産経新聞【 速報 】":
                res = requests.get("https://www.sankei.com/flash/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # 産経新聞【 社会 】
            elif target_site == "産経新聞【 社会 】":
                res = requests.get("https://www.sankei.com/affairs/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # 産経新聞【 政治 】
            elif target_site == "産経新聞【 政治 】":
                res = requests.get("https://www.sankei.com/politics/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # 産経新聞【 国際 】
            elif target_site == "産経新聞【 国際 】":
                res = requests.get("https://www.sankei.com/world/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # 産経新聞【 経済 】
            elif target_site == "産経新聞【 経済 】":
                res = requests.get("https://www.sankei.com/economy/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # 産経新聞【 スポーツ 】
            elif target_site == "産経新聞【 スポーツ 】":
                res = requests.get("https://www.sankei.com/sports/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # 産経新聞【 エンタメ 】
            elif target_site == "産経新聞【 エンタメ 】":
                res = requests.get("https://www.sankei.com/entertainments/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # 産経新聞【 ライフ 】
            elif target_site == "産経新聞【 ライフ 】":
                res = requests.get("https://www.sankei.com/life/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # 産経新聞【 イベント 】
            elif target_site == "産経新聞【 イベント 】":
                res = requests.get("https://www.sankei.com/event/")
                soup = bs4(res.content, "lxml")
                h2 = soup.find('h2', class_="headline")
                a = h2.find('a')
                url = a.get('href')
                url = "https://www.sankei.com/" + url
                Scraping(".article-body p" , target_site)
            # Yahoo!【 主要 】
            elif target_site == "Yahoo!【 主要 】":
                res = requests.get("https://news.yahoo.co.jp/topics/top-picks")
                soup = bs4(res.content, "lxml")
                a = soup.find('a', class_="newsFeed_item_link")
                url = a.get('href')
                res = requests.get(url)
                soup = bs4(res.content, "lxml")
                p = soup.find('p', class_="sc-kvjbNB")
                a = p.find('a')
                url = a.get('href')
                print(url)
                Scraping(".article_body p" , target_site)
            # Yahoo!【 国内 】
            elif target_site == "Yahoo!【 国内 】":
                res = requests.get("https://news.yahoo.co.jp/topics/domestic")
                soup = bs4(res.content, "lxml")
                a = soup.find('a', class_="newsFeed_item_link")
                url = a.get('href')
                res = requests.get(url)
                soup = bs4(res.content, "lxml")
                p = soup.find('p', class_="sc-kvjbNB")
                a = p.find('a')
                url = a.get('href')
                print(url)
                Scraping(".article_body p" , target_site)
            # Yahoo!【 国際 】
            elif target_site == "Yahoo!【 国際 】":
                res = requests.get("https://news.yahoo.co.jp/topics/world")
                soup = bs4(res.content, "lxml")
                a = soup.find('a', class_="newsFeed_item_link")
                url = a.get('href')
                res = requests.get(url)
                soup = bs4(res.content, "lxml")
                p = soup.find('p', class_="sc-kvjbNB")
                a = p.find('a')
                url = a.get('href')
                print(url)
                Scraping(".article_body p" , target_site)
            # Yahoo!【 経済 】
            elif target_site == "Yahoo!【 経済 】":
                res = requests.get("https://news.yahoo.co.jp/topics/business")
                soup = bs4(res.content, "lxml")
                a = soup.find('a', class_="newsFeed_item_link")
                url = a.get('href')
                res = requests.get(url)
                soup = bs4(res.content, "lxml")
                p = soup.find('p', class_="sc-kvjbNB")
                a = p.find('a')
                url = a.get('href')
                print(url)
                Scraping(".article_body p" , target_site)
            # Yahoo!【 エンタメ 】
            elif target_site == "Yahoo!【 エンタメ 】":
                res = requests.get("https://news.yahoo.co.jp/topics/entertainment")
                soup = bs4(res.content, "lxml")
                a = soup.find('a', class_="newsFeed_item_link")
                url = a.get('href')
                res = requests.get(url)
                soup = bs4(res.content, "lxml")
                p = soup.find('p', class_="sc-kvjbNB")
                a = p.find('a')
                url = a.get('href')
                print(url)
                Scraping(".article_body p" , target_site)
            # Yahoo!【 スポーツ 】
            elif target_site == "Yahoo!【 スポーツ 】":
                res = requests.get("https://news.yahoo.co.jp/topics/sports")
                soup = bs4(res.content, "lxml")
                a = soup.find('a', class_="newsFeed_item_link")
                url = a.get('href')
                res = requests.get(url)
                soup = bs4(res.content, "lxml")
                p = soup.find('p', class_="sc-kvjbNB")
                a = p.find('a')
                url = a.get('href')
                print(url)
                Scraping(".article_body p" , target_site)
            # Yahoo!【 IT 】
            elif target_site == "Yahoo!【 IT 】":
                res = requests.get("https://news.yahoo.co.jp/topics/it")
                soup = bs4(res.content, "lxml")
                a = soup.find('a', class_="newsFeed_item_link")
                url = a.get('href')
                res = requests.get(url)
                soup = bs4(res.content, "lxml")
                p = soup.find('p', class_="sc-kvjbNB")
                a = p.find('a')
                url = a.get('href')
                print(url)
                Scraping(".article_body p" , target_site)
            # Yahoo!【 科学 】
            elif target_site == "Yahoo!【 科学 】":
                res = requests.get("https://news.yahoo.co.jp/topics/science")
                soup = bs4(res.content, "lxml")
                a = soup.find('a', class_="newsFeed_item_link")
                url = a.get('href')
                res = requests.get(url)
                soup = bs4(res.content, "lxml")
                p = soup.find('p', class_="sc-kvjbNB")
                a = p.find('a')
                url = a.get('href')
                print(url)
                Scraping(".article_body p" , target_site)
            # Yahoo!【 ライフ 】
            elif target_site == "Yahoo!【 ライフ 】":
                res = requests.get("https://news.yahoo.co.jp/topics/life")
                soup = bs4(res.content, "lxml")
                a = soup.find('a', class_="newsFeed_item_link")
                url = a.get('href')
                res = requests.get(url)
                soup = bs4(res.content, "lxml")
                p = soup.find('p', class_="sc-kvjbNB")
                a = p.find('a')
                url = a.get('href')
                print(url)
                Scraping(".article_body p" , target_site)
            # Yahoo!【 地域 】
            elif target_site == "Yahoo!【 地域 】":
                res = requests.get("https://news.yahoo.co.jp/topics/local")
                soup = bs4(res.content, "lxml")
                a = soup.find('a', class_="newsFeed_item_link")
                url = a.get('href')
                res = requests.get(url)
                soup = bs4(res.content, "lxml")
                p = soup.find('p', class_="sc-kvjbNB")
                a = p.find('a')
                url = a.get('href')
                print(url)
                Scraping(".article_body p" , target_site)
            elif target_site == "CNN【 World 】":
                res = requests.get("https://www.cnn.co.jp/world/")
                soup = bs4(res.content, "lxml")
                ul = soup.find('ul', class_="list-news-line")
                li = ul.find('li')
                a = li.find('a')
                url = a.get('href')
                url = "https://www.cnn.co.jp/" + url
                print(url)
                Scraping("#leaf-body p" , target_site)
            elif target_site == "CNN【 USA 】":
                res = requests.get("https://www.cnn.co.jp/usa/")
                soup = bs4(res.content, "lxml")
                ul = soup.find('ul', class_="list-news-line")
                li = ul.find('li')
                a = li.find('a')
                url = a.get('href')
                url = "https://www.cnn.co.jp/" + url
                print(url)
                Scraping("#leaf-body p" , target_site)
            elif target_site == "CNN【 Business 】":
                res = requests.get("https://www.cnn.co.jp/business/")
                soup = bs4(res.content, "lxml")
                ul = soup.find('ul', class_="list-news-line")
                li = ul.find('li')
                a = li.find('a')
                url = a.get('href')
                url = "https://www.cnn.co.jp/" + url
                print(url)
                Scraping("#leaf-body p" , target_site)
            elif target_site == "CNN【 Tech 】":
                res = requests.get("https://www.cnn.co.jp/tech/")
                soup = bs4(res.content, "lxml")
                ul = soup.find('ul', class_="list-news-line")
                li = ul.find('li')
                a = li.find('a')
                url = a.get('href')
                url = "https://www.cnn.co.jp/" + url
                print(url)
                Scraping("#leaf-body p" , target_site)
            elif target_site == "CNN【 Entertainment 】":
                res = requests.get("https://www.cnn.co.jp/showbiz/")
                soup = bs4(res.content, "lxml")
                ul = soup.find('ul', class_="list-news-line")
                a = ul.find('a')
                url = a.get('href')
                url = "https://www.cnn.co.jp/" + url
                print(url)
                Scraping("#leaf-body p" , target_site)
            elif target_site == "CNN（ World ） - EN":
                res = requests.get("https://edition.cnn.com/world")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="cd__headline")
                a = h3.find('a')
                url = a.get('href')
                url = "https://edition.cnn.com" + url
                print(url)
                Scraping(".zn-body__paragraph" , target_site)
            elif target_site == "CNN（ USA ） - EN":
                res = requests.get("https://edition.cnn.com/politics")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="cd__headline")
                a = h3.find('a')
                url = a.get('href')
                url = "https://edition.cnn.com" + url
                print(url)
                Scraping(".zn-body__paragraph" , target_site)
            elif target_site == "CNN（ Business ） - EN":
                res = requests.get("https://edition.cnn.com/business")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="cd__headline")
                a = h3.find('a')
                url = a.get('href')
                url = "https://edition.cnn.com" + url
                print(url)
                Scraping(".zn-body__paragraph" , target_site)
            elif target_site == "CNN（ Sports ） - EN":
                res = requests.get("https://edition.cnn.com/sports")
                soup = bs4(res.content, "lxml")
                a = soup.find('a', class_="container_lead-plus-headlines__link")
                url = a.get('href')
                print(url)
                Scraping(".zn-body__paragraph" , target_site)
            elif target_site == "CNN（ Entertainment ） - EN":
                res = requests.get("https://edition.cnn.com/entertainment")
                soup = bs4(res.content, "lxml")
                h3 = soup.find('h3', class_="cd__headline")
                a = h3.find('a')
                url = a.get('href')
                url = "https://edition.cnn.com" + url
                print(url)
                Scraping(".zn-body__paragraph" , target_site)
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
        print("英語の記事です！")
    else:
        hoge = gTTS(data,lang="ja")
    rannum = random.uniform(0,10000)    
    hoge.save(f"static/files/audio/article{rannum}.mp3")
    f.close()

    def get_title(t):
        res = requests.get(url)
        soup = bs4(res.content , "lxml")
        t.title = soup.find("title").text

    t = TITLE()
    get_title(t)
    # 最新の履歴データのIDを取得
    articleID = database.count()
    return render_template('result.html', result=data, url = url , title = t.title , articleID=articleID[0] , rannum = rannum)
if __name__ == '__main__':
    app.run()   
    






