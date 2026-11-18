# enshu-lifehack-hamamatsu

浜松ライフハック（遠州ライフハック 浜松市版）の **静的サイト** リポジトリ。
公開先：`https://hamamatsu.enshu-lifehack.com/`（Cloudflare Workers Static Assets）

湖西版から手動クローン・履歴を切って新設。横展開の設計原則は袋井版の指示書（`enshu-lifehack-fukuroi` リポジトリ `docs/fukuroi-lifehack-design-spec.md`）に準拠する。

## 構成

静的HTMLのみ。Cloudflare の **Build output directory = `/`**（ビルド不要）で配信する。

```
index.html              トップ（くらしの場面・目的から選ぶ）
data/city.json          市プロファイル（市名・公式窓口・CVフラグ等の差分を集約）
data/topics_master.json 中項目マスター台帳（磐田155項目が起点）
data/content/<category>.json 中項目ごとの執筆済みコンテンツ（qa/steps/tabs等）
life/<大項目>/           くらしの大項目ページ
life/<大項目>/<中項目>/   個別ページ
sitemap.xml             サイトマップ
robots.txt
_redirects              旧 /iwata/ 配下 → 直下への 301
404.html                カスタム404
favicon.svg
```

## 生成方法

本サイトは公式サイトのクロール・静的化ではなく、`data/topics_master.json` の中項目台帳をもとに、公式情報を1件ずつ調査した上でAIが執筆する「台帳駆動」の生成物である（掛川版・森町版と同じ方式）。

## 免責

本サイトは浜松市公式サイトではありません。最新・正確な情報は浜松市公式サイトをご確認ください。
運営：富士ヶ丘サービス ／ 代表：大石浩之

# 2026年11月18日以降の編集・再生成

全体の再生成は `python scripts/build-all.py`。既存の158案内に加え、トップ、目的別ガイド3件、全件検索、更新記録、運営者案内、サイトマップ、検索索引を同期する。

- 既存案内の原稿：`data/content/*.json`、基本項目・出典：`data/topics_master.json`
- 目的別ガイド・トップの更新案内：`data/guide-hubs.json`
- 今回確認した補足は `update.checked`、`supplement_checked_date` で管理。既存の基礎情報の確認日を一括更新しない。
- 期限付き案内の `end` は日本時間の日付で終了表示に切り替わる。公式の受付状況を取得する仕組みではない。新年度の期限を推測で繰り上げない。
- チェックリストはブラウザのlocalStorageのみを使用する。保存キーに紐付く項目の順番を変える際は既存チェックの意味を保持するかキーのバージョンを更新する。
- 検査：`python scripts/inspect_all.py`、`node scripts/test-search.mjs`、`node scripts/check-synonyms.mjs`。公開前後に新規導線、検索、PC・狭幅の実ブラウザ表示も確認する。
- 2026-11-18の補足・出典修正を重複追加しない。差分と `reports/2026-11-18-update.md` を参照し、最新mainと公式原文を照合して編集する。


## トップの写真館・富士ヶ丘サービス相談案内（2026-11-19）

`parts/community-links.html` がトップページの案内の原本です。`index.html` の `PART:community-links` マーカーへ同期してください。写真館は実在する市町だけに掲載し、他市町の館をその市町の写真館として表示しません。実家カルテと介護相談は市町別UTM・クリック計測付きです。行政案内・既存のガイド・各自治体公式へのリンクを保持してください。相談写真は運営会社の既存サイトに掲載された写真です。
