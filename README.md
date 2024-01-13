# 情報活用力測定ツール

このプロジェクトは、学生が自身の情報通信技術に関する知識やスキルを評価し、把握するためのWEBツールです。主にFlaskを用いてバックエンドを構築し、フロントエンドではHTML、CSS、JavaScriptなどを使用しています。また、結果の可視化にはPlotly.jsが利用されています。

## 概要
このツールの目的は、学生自身が現時点での情報通信技術に関する知識やスキルの特徴を明らかにし、改善の方向性を示すことです。ユーザーは様々なカテゴリに関する質問に回答し、その結果がPlotly.jsを用いて視覚的に表現されます。

## 主な機能
- ログイン機能
- ユーザーが所属する大学や学年、学科などの情報の登録
- 情報活用力を全66門の質問を通してチェックする
  - オンラインコラボレーション力（15項目）
  - データ利活用力（15項目）
  - 情報システム開発力（14項目）
  - 情報倫理力（22項目）
- カテゴリごとの正答の割合をレーダーチャートで描画
- 設問ごとの自分の回答結果と回答割合の確認


## 技術スタック
- バックエンド: Flask
- フロントエンド: HTML, CSS, JavaScript
- データの可視化: Plotly.js

## ローカルでの実行方法
1. このリポジトリをクローンします。


```
git clone https://github.com/your-username/your-repo.git
```

2. 依存関係をインストールします。

```
pip install -r requirements.txt
```

3. Flaskアプリケーションを起動します。

```
python app.py
```

4. ブラウザで http://127.0.0.1:5000/ にアクセスします。

## 貢献
このプロジェクトに興味を持った方は、プルリクエストやイシューを通じて貢献していただけると嬉しいです。お気軽にご参加ください！#   I n u s 
 
 
