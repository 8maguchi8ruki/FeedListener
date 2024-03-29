<img style="width:300px;" src="https://user-images.githubusercontent.com/77283970/231783718-2fdef319-79be-4b7f-8f0b-16b7af5e1fa3.png">

<h3>DEMO</h3>

https://user-images.githubusercontent.com/77283970/233369520-50a32a23-4253-4d53-9b34-ce8715b0a007.mp4


<p>
Web記事の読み上げに特化した音声読み上げアプリケーションです。
</p>

 <p> 
📱スマートフォンでの利用を推奨しています。
</p>

 <a href="https://www.feed-listener.com/home/1762">https://www.feed-listener.com/home/1762</a>

（テストアカウントでログイン済みです）


<hr>

<h3>Feed Listenerの特徴</h3>
<p>feedlyというRSSリーダーを利用していて、記事を読む際にスマホを見なければならないのが億劫に感じたため、読み上げアプリをいろいろ試していました。しかしどの読み上げアプリも上手に読んでくれず、ないなら自分で作っちゃおう！と思って開発しているのがこのアプリです。ではgoogle読み上げのようなものと何が違うのか、それは必要ない情報を排除して読み上げるところです。</p>


<h4>Googleアシスタントの音声読み上げは意外とポンコツ</h4>


https://user-images.githubusercontent.com/77283970/233316468-8edec598-2bcc-44fb-abb8-02ad116bf7ad.mp4



<br>

Googleアシスタントはこのような感じで、いきなり「エイチティーティーピーコロンスラッシュスラッシュ...」と読み上げます。
私は記事の内容が知りたいのでリンクを読まれては困りますし、なにより肝心の内容が頭に入ってきません。

Feed Listenerでは、こういった記事中の不要な部分を取り除いて音声ファイルを出力することで、使いやすい読み上げ機能を実現しました。
下記の画像の通り、リンクと引用の文字列が取り除かれていることが確認できるかと思います。
<br>


<div>
  <img style="width:350px;" src="https://user-images.githubusercontent.com/77283970/231784525-84c7cd6e-2434-4530-a220-498d3aef6bba.jpg">
  <img style="width:350px;" src="https://user-images.githubusercontent.com/77283970/231784542-8028fcc8-ef06-4d2f-a143-af75c5b499e6.jpg">
</div>

<br>

この機能は正規表現をうまく活用して制作しています。BeautifulSoupというPythonライブラリを用いてスクレイピングを行い、取ってきたデータをパースします。
BeautifulSoupが返すデータには改行文字列(\n)も含むため、改行文字列ごとに文章を区切り、それぞれの文に対して正規表現を用いて排除判定しています。
排除対象は主に、( https:// )から始まるリンクや、英単語三文字以上で構成された英文です。

<br>

<img width="688" alt="スクリーンショット 2023-04-18 16 12 35" src="https://user-images.githubusercontent.com/77283970/232699861-5d902d66-badc-465c-9b4e-7096c0a47c9d.png">

<hr>

<h3>基本操作</h3>

<p>
基本操作は以下の3ステップ。(冒頭のDEMO動画を見ていただくのがわかりやすいかと思います。)

<h4>Step1</h4>
まずお使いのGoogleアカウントでログインします。
<h4>Step2</h4>
ホーム画面のマイリストからマイリストページへ移動します。マイリストページの右上のプラスボタンを押し、追加したいサイトを選択してマイリストを作成します。
<h4>Step3</h4>
マイリストの登録が完了したらホーム画面に戻り、【最新記事】および【URLで調べる】が利用可能になります。
（【最新記事】は選択されたサイトの最新記事の音声ファイルを出力します。【URLで検索】の場合は読み上げ対象の記事URLを検索フォームに入力する必要があります。）
</p>

<hr>

<h3>アーカイブ機能について</h3>
<img width="500" alt="スクリーンショット 2023-04-20 21 01 20" src="https://user-images.githubusercontent.com/77283970/233360144-d8d96c83-a734-43db-8d3b-2f1f514f37b5.png">


お気に入りの記事、再度聴きたい記事を保存しておくことができます。

【もう一度】ボタンを押すと、対象の記事の音声ファイルを再度作成します。

アーカイブに保存しておけば、再度聴きたいときに、対象の記事URLを探す手間がなくなるのでとても便利です。ぜひご活用ください。

なお、必要がなくなった時は右端の削除ボタンから削除することができます。
<br>


<hr>
<h3>使用した技術</h3>
<h4>フロントエンド</h4>
HTML,CSS(Sass),JavaScript(Vue.js)
<h4>バックエンド</h4>
Python(Flask),SQlite3,Heroku
<h4>その他（ツール,API,ライブラリなど）</h4>
Git,VScode,Google OAuth,gTTS,BeutifulSoup　

<hr>
