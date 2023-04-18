import sqlite3
from tokenize import String
from markupsafe import string



##### ユーザー登録 #####
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

##### ユーザー参照 #####
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

##### ユーザー削除 #####
def delete_user(sitename):
    print(sitename)
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    # c.execute("DELETE FROM my_site")
    c.execute('DELETE FROM my_site WHERE sitename = "{}"'.format(sitename))
    conn.commit()
    c.close()
    conn.close()





##### 履歴表作成 #####
def history_create():
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS historys(id INTEGER PRIMARY KEY AUTOINCREMENT , user_id STRING ,title STRING , url STRING)')
    conn.commit()
    c.close()
    conn.close()

##### 履歴表更新 #####
def history_update(current_user,title,url):
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS historys(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id STRING , title STRING , url STRING)')
    c.execute('INSERT INTO historys(user_id,title,url) VALUES(?,?,?)',[current_user,title,url])
    conn.commit()
    c.close()   
    conn.close()
    return

##### 履歴表参照 #####
def history_select(current_user):
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
def delete_history(current_user):
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute(f'DELETE FROM historys WHERE user_id = {current_user}') 
    conn.commit()
    c.close()
    conn.close()
    return

##### 履歴表から最新のレコードIDを取得 #####
def count():
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('SELECT MAX(id) FROM historys')
    result = c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return result





##### アーカイブ表作成 #####
def archive_create():
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS archives(id INTEGER PRIMARY KEY AUTOINCREMENT , user_id STRING ,title STRING , url STRING)')
    conn.commit()
    c.close()
    conn.close()

##### アーカイブ登録 #####
def archive_up(articleID,current_user):
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
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
def delete_archives(current_user):
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute(f'DELETE FROM archives WHERE user_id = {current_user}') 
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





##### マイリスト登録 #####
def update_site(current_user , name):
    datas = []
    print(name)
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS my_site(user_id STRING , sitename STRING)')
    c.execute('INSERT INTO my_site(user_id,sitename) VALUES(?,?)',[current_user ,name])
    for row in c:
        datas.append(row)
    print("登録されているか")
    print(datas)
    conn.commit()
    c.close()
    conn.close()

##### マイリスト削除 #####
def delete_site(current_user , sitename):
    print(current_user , sitename)
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('DELETE FROM my_site WHERE sitename = "{}"'.format(sitename))
    conn.commit()
    c.close()
    conn.close()

##### マイリスト参照 #####
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





##### 問い合わせユーザー表 #####
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





###### 全サイト表作成 #####
def create_all_site():
    conn = sqlite3.connect('fr_db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS all_site(sitename STRING PRIMARY KEY)')
    c.execute('INSERT INTO all_site(sitename) VALUES("産経新聞【社会】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("産経新聞【政治】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("産経新聞【国際】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("産経新聞【経済】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("産経新聞【スポーツ】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("産経新聞【エンタメ】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIZMODO【テクノロジ】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIZMODO【サイエンス】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIZMODO【プロダクト】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIZMODO【エンタメ】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIZMODO【ライフ】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIZMODO【ビジネス】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN【国際】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN【アメリカ】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN【ビジネス】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN【テクノロジ】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("CNN【エンタメ】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIGAZINE【アプリ】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIGAZINE【サービス】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIGAZINE【サイエンス】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIGAZINE【ゲーム】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIGAZINE【映画】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIGAZINE【アニメ】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIGAZINE【生物】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("GIGAZINE【レビュー】") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("TechCrunch【AI】-EN") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("TechCrunch【Crypto】-EN") ON CONFLICT (sitename) DO NOTHING')
    c.execute('INSERT INTO all_site(sitename) VALUES("TechCrunch【Startups】-EN") ON CONFLICT (sitename) DO NOTHING')

    conn.commit()
    c.close()
    conn.close()

##### 全サイト表参照 #####
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