import sqlite3
from tokenize import String

from markupsafe import string

##### 履歴表更新 #####
def update(current_user,title,url):
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS historys(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id STRING , title STRING , url STRING)')
    c.execute('INSERT INTO historys(user_id,title,url) VALUES(?,?,?)',[current_user,title,url])
    conn.commit()
    c.close()   
    conn.close()
    return

##### 履歴表参照 #####
def select(current_user):
    datas = []
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM historys WHERE user_id = {current_user}')
    for row in c:
        datas.append(row)
    conn.commit()
    c.close()
    conn.close()
    return datas

##### 履歴表削除 #####
def delete_historys(current_user):
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute(f'DELETE FROM historys WHERE user_id = {current_user}') 
    conn.commit()
    c.close()
    conn.close()
    return

##### 最新のレコードIDを取得 #####
def count():
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    # c.execute('CREATE TABLE IF NOT EXISTS historys(id INTEGER PRIMARY KEY AUTOINCREMENT, title STRING , url STRING)')
    c.execute('SELECT MAX(id) FROM historys')
    result = c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return result

##### アーカイブ保存 #####
def archive_up(articleID,current_user):
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    # アーカイブ表を作成
    c.execute('CREATE TABLE IF NOT EXISTS archives(id INTEGER PRIMARY KEY AUTOINCREMENT , user_id STRING ,title STRING , url STRING)')
    # アーカイブ対象レコードをアーカイブ表に追加
    c.execute('SELECT * FROM historys WHERE id = {}'.format(articleID))
    result = c.fetchall()
    print("テスト")
    print(result)
    title = result[0][2]
    url = result[0][3]
    print(title,url)
    c.execute('INSERT INTO archives(id,user_id,title,url) VALUES(?,?,?,?)',[articleID,current_user,title,url])  
    conn.commit()
    c.close()
    conn.close()
    return "done!!"

##### アーカイブ参照 #####
def archive_sl(current_user):
    datas = []
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM archives WHERE user_id = {current_user}') 
    for row in c:
        datas.append(row)
    print(datas)
    c.close()
    conn.close()
    return datas

##### アーカイブ全削除 #####
def delete_archives():
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('DELETE FROM archives') 
    conn.commit()
    c.close()
    conn.close()
    return

##### アーカイブ個別削除 #####
def delete_this(articleID):
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('DELETE FROM archives WHERE id = {}'.format(int(articleID))) 
    conn.commit()
    c.close()
    conn.close()
    return

# 問い合わせユーザー表
def contact_user(name,email,text):
    datas = []
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS contact_user(id INTEGER PRIMARY KEY AUTOINCREMENT ,name STRING , email STRING ,text STRING)')
    c.execute('INSERT INTO contact_user(name,email,text) VALUES(?,?,?)',[name,email,text])  
    c.execute('SELECT * FROM contact_user') 
    for row in c:
        datas.append(row)
    print(datas)
    conn.commit()
    c.close()
    conn.close()
    return "done!!"


# 全サイト表作成
def create_all_site():
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    # c.execute("DELETE FROM all_site")
    c.execute('CREATE TABLE IF NOT EXISTS all_site(id INTEGER PRIMARY KEY , sitename STRING)')
    c.execute('INSERT INTO all_site(sitename) VALUES("Yahoo!【 主要 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("Yahoo!【 国内 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("Yahoo!【 国際 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("Yahoo!【 スポーツ 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("Yahoo!【 エンタメ 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("Yahoo!【 経済 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("Yahoo!【 IT 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("Yahoo!【 科学 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("Yahoo!【 ライフ 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("産経新聞【 社会 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("産経新聞【 政治 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("産経新聞【 国際 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("産経新聞【 経済 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("産経新聞【 スポーツ 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("産経新聞【 エンタメ 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("産経新聞【 ライフ 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIZMODO【 テクノロジ 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIZMODO【 サイエンス 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIZMODO【 プロダクト 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIZMODO【 エンタメ 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIZMODO【 ライフ 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIZMODO【 ビジネス 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN【 World 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN【 USA 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN【 Business 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN【 Tech 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN【 Entertainment 】")')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN（ World ） - EN")')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN（ USA ） - EN")')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN（ Business ） - EN")')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN（ Sports ） - EN")')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN（ Entertainment ） - EN")')
    c.execute('INSERT INTO all_site(sitename) VALUES("Techcrunch【 Startup 】 - EN")')
    c.execute('INSERT INTO all_site(sitename) VALUES("Premierleague - EN")')
    conn.commit()
    c.close()
    conn.close()

# 全サイト表参照
def select_all_site(current_user):
    datas = []
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS all_site(id INTEGER PRIMARY KEY , sitename STRING)')
    c.execute('SELECT DISTINCT * FROM all_site') 
    for row in c:
        datas.append(row)
    print(datas)
    conn.commit()
    c.close()
    conn.close()
    return datas

# マイサイト表登録
def update_site(current_user , name):
    datas = []
    print(name)
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    # c.execute("DELETE FROM my_site")
    c.execute('CREATE TABLE IF NOT EXISTS my_site(user_id STRING , sitename STRING)')
    c.execute('INSERT INTO my_site(user_id,sitename) VALUES(?,?)',[current_user ,name])
    for row in c:
        datas.append(row)
    print("登録されているか")
    print(datas)
    conn.commit()
    c.close()
    conn.close()

def delete_site(current_user , sitename):
    print(current_user , sitename)
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    # c.execute("DELETE FROM my_site")
    c.execute('DELETE FROM my_site WHERE sitename = "{}"'.format(sitename))
    conn.commit()
    c.close()
    conn.close()

# マイサイト表参照
def select_site(current_user):
    datas = []
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS my_site(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id STRING ,sitename STRING)')
    c.execute(f'SELECT DISTINCT * FROM my_site WHERE user_id = {current_user}') 
    for row in c:
        datas.append(row)
    print("テスト")
    print(datas)
    conn.commit()
    c.close()
    conn.close()
    return datas




# ユーザー登録
def update_user(user_id , user_name , user_photo):
    datas = []
    print(user_id , user_name , user_photo)
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS all_user(user_id STRING PRIMARY KEY ,user_name STRING , user_photo STRING)')
    c.execute(f'REPLACE INTO all_user(user_id ,user_name , user_photo) VALUES(?,?,?) ON CONFLICT (user_id) DO NOTHING',[user_id , user_name , user_photo])
    for row in c:
        datas.append(row)
    print(datas)
    conn.commit()
    c.close()
    conn.close()


# ユーザー参照
def select_user():
    datas = []
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS all_user(user_id STRING ,user_name STRING , user_photo STRING)')
    c.execute(f'SELECT * FROM all_user') 
    #  WHERE user_id = {user_id}
    for row in c:
        datas.append(row)
    print(datas)
    conn.commit()
    c.close()
    conn.close()
    return datas

def delete_user(sitename):
    print(sitename)
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    # c.execute("DELETE FROM my_site")
    c.execute('DELETE FROM my_site WHERE sitename = "{}"'.format(sitename))
    conn.commit()
    c.close()
    conn.close()