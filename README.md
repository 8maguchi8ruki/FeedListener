<img style="width:300px;" src="https://user-images.githubusercontent.com/77283970/231783718-2fdef319-79be-4b7f-8f0b-16b7af5e1fa3.png">

<p>
Web記事の読み上げに特化した音声読み上げアプリケーションです。
</p>

 <a href="https://www.feed-listener.com">https://www.feed-listener.com</a>

 <p style="color:red;"> 
📱＊スマートフォンでの利用を推奨しています。
  
📱＊利用するにはログインが必要です。
</p>


<hr>

<h3>Feed Listenerの特徴</h3>
<h4>Googleアシスタントの音声読み上げは意外とポンコツ</h4>

<video src="https://user-images.githubusercontent.com/77283970/231780953-1064b3a8-1f58-4474-96c3-b06916ef3507.mp4"></video>

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

<img width="683" alt="スクリーンショット 2023-04-17 15 49 07" src="https://user-images.githubusercontent.com/77283970/232406292-19656b21-47c7-420e-823f-da4a1a6a7c77.png">

<hr>

<h3>使い方</h3>

<p>
使い方は至ってシンプルです。下記のDEMOを見ていただくのがわかりやすいかと思います。
まず、ホーム画面のマイリストを選択します。
その後、マイリストページの【+】ボタンからお気に入りのサイトを追加します。
追加が完了したらホーム画面の『最新記事』、『URLで検索』を選択することで対象の記事の音声ファイルが出力されます。
（『URLで検索』の場合は対象のURLを入力する必要があります。）
</p>

<h3>HOW TO USE</h3>

<p>
This is simple. 
First of all, select mylist from the menu.
and then You just have to add your favorite site from plus button.
after this, You can select recent post and url search button.
that's it !!
You can easily to listen Web article whenever you want.
When you don't need your favorite site and you want to delete it, of couse it can be deleted. 
please push the delete button on the right.👍
</p>

<h3>DEMO</h3>
<video src="https://user-images.githubusercontent.com/77283970/231787433-9ee8e1cf-c4de-474a-a442-5153d6020fd6.mp4"></video>

<br>
