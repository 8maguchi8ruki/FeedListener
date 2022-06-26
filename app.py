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

app = Flask(__name__)
rannum = ""
##### トップページ #####
@app.route('/')
def index():
    print(rannum)

    if os.path.exists("static/files/audio"):
        print("audioフォルダを削除しました")
        shutil.rmtree("static/files/audio")

    return render_template('index.html')

##### トップページ全サイト取得ajax #####
@app.route('/ajax/all_site/')
def all_site():
    return jsonify(database.select_all_site())

# トップページサイト追加ajax
@app.route('/ajax/add_site/<sitename>')
def add_site(sitename):
    database.update_site(sitename)
    return jsonify(database.select_site())

# トップページサイト削除ajax
@app.route('/ajax/delete_site/<sitename>')
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
    return render_template("recent.html")


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
@app.route('/contact_success/', methods=['GET','POST'])
def contact_success():
    name = request.form.get('name')
    email = request.form.get('email')
    text = request.form.get('textarea')
    print(name,email,text)
    contact_me.send(name,email,text)
    return render_template("contact_success.html")

##### 履歴ページ #####
@app.route('/history/')
def history():
    datas = database.select()
    return render_template('history.html',datas = datas)

##### 履歴全削除ajax #####
@app.route('/ajax/delete_historys/', methods=['GET'])
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
@app.route('/ajax/delete_archives/', methods=['GET'])
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
    elif "jp.techcrunch.com" in url:
        sitename = "techcrunch"
        Scraping(".article-entry.text p" , sitename)
    #GIZMODO
    elif "gizmodo.jp" in url:
        sitename = "gizmodo"
        Scraping(".p-post-content p" , sitename)
    # CoinPost
    elif "coinpost.jp" in url:
        sitename = "coinpost"
        Scraping(".entry-content p", sitename)
    # telektlist
    elif "telektlist.com" in url:
        sitename = "telektlist"
        Scraping(".entry-content p", sitename)
    # VAIENCE
    elif "vaience.com" in url:
        sitename = "vaience"
        Scraping(".entry-content p", sitename)
    # 朝日新聞
    elif "asahi.com" in url:
        sitename = "asahi"
        Scraping(".nfyQp p" , sitename)
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
    # ITmedia
    elif "itmedia.co.jp" in url:
        sitename = "itmedia"
        Scraping(".inner p" , sitename)
    # GIGAZINE
    elif "gigazine.net" in url:
        sitename = "gigazine"
        Scraping(".preface" , sitename)
    
    # 最新の投稿
    elif url == "new_post":
            target_site = request.form.get('target_site')
            print(target_site)
            # Cnet
            if target_site == "Cnet":
                res = requests.get("https://japan.cnet.com/release/")
                soup = bs4(res.content, "lxml")
                a = soup.find('a', class_="bold")
                recent_post = a.get('href')
                url = "https://japan.cnet.com/" + recent_post
                Scraping(".article_body p" , target_site)
                
    else:
        return render_template("404.html")

 
    #article.txtをarticle.mp3へ変換
    print("----- 記事情報取得中 -----")
    time.sleep(2)
    f = open(path, 'r',encoding="UTF-8")
    print("----- 音声ファイル作成中 -----")
    data = f.read()
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
    






