"""Build the home, purpose routes, complete directory and dated update log.
No network access: editorial input lives in data/guide-hubs.json and content/*.json.
"""
import json,re,html
from datetime import date
from pathlib import Path
from photo_referrals import HOME_PHOTOS, VISIT_PHOTOS
from share_metadata import share_metadata
R=Path(__file__).resolve().parent.parent
H=json.loads((R/'data/guide-hubs.json').read_text(encoding='utf-8'))
T=json.loads((R/'data/topics_master.json').read_text(encoding='utf-8'))
CAT=json.loads((R/'data/categories.json').read_text(encoding='utf-8'))['categories']
SITE='https://hamamatsu.enshu-lifehack.com'
CURRENT = date.fromisoformat(H['checked'])
DISPLAY_DATE = f'{CURRENT.year}年{CURRENT.month}月{CURRENT.day}日'
def esc(v):return html.escape(str(v),quote=True)
def life(s):return '/life/'+s+'/'
def card(link,title,body='',icon='',compact=False):
 return f'<a class="guide-card" href="{esc(link)}"><span class="icon" aria-hidden="true">{icon}</span><strong>{esc(title)}</strong><small>{esc(body)}</small><span class="arrow" aria-hidden="true">詳しく見る →</span></a>'
def layout(path,title,description,body,home=False):
 old=(R/'index.html').read_text(encoding='utf-8')
 bing=re.search(r'<meta name="msvalidate.01"[^>]*>',old)
 headmeta=bing.group() if home and bing else ''
 header=(R/'parts/header.html').read_text(encoding='utf-8').strip()
 footer=(R/'parts/footer.html').read_text(encoding='utf-8').strip()
 return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | 浜松ライフハック</title><meta name="description" content="{esc(description)}">{headmeta}
<link rel="canonical" href="{SITE}{path}"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
{share_metadata(SITE,path,title+' | 浜松ライフハック',description)}
<!-- PART:head-css:START --><link rel="stylesheet" href="/assets/site.css?v=20260705a"><!-- PART:head-css:END -->
<link rel="stylesheet" href="/assets/resident-guide.css?v={'20261124' if home else '20261118'}"></head><body class="hub {'home' if home else 'guide-body'}">
<a href="#main" class="skip-link">本文へ移動</a><!-- PART:header:START -->{header}<!-- PART:header:END -->
<div class="notice"><div class="wrap">浜松市公式サイトではありません。手続き・申請の最終確認は各ページの公式窓口へ。</div></div>
<main id="main"><div class="wrap">{body}
<nav class="guide-nav" aria-label="サイト案内"><a href="/">トップ</a><a href="/guides/">全ガイドを探す</a><a href="/updates/">確認した最新情報</a><a href="/about/">運営者・編集方針</a></nav>
</div></main><!-- PART:footer:START -->{footer}<!-- PART:footer:END -->
<script defer src="/assets/resident-guide.js"></script><script type="module" src="/assets/search-app.js"></script></body></html>'''
def write(path,title,desc,body,home=False):
 p=R/path.strip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(layout(path,title,desc,body,home),encoding='utf-8',newline='\n')
def news(archive=False):
 out=[]
 for n in H['news']:
  expired=bool(n.get('end') and n['end'] < H['checked'])
  if expired != archive:
   continue
  end=f' data-end-date="{n["end"]}"' if n.get('end') else ''
  out.append(f'<article class="news-item"{end}><span class="news-status">{esc(n["label"])}</span><h3><a href="{life(n["path"])}#guide-update">{esc(n["title"])}</a></h3><p>{esc(n["summary"])}</p><small>確認日：{esc(n.get("checked",H["checked"]))}</small></article>')
 return '<div class="news-list">'+''.join(out)+'</div>'

purpose='<div class="guide-grid">'+''.join(card('/guides/'+g['slug']+'/',g['title'],g['description'],g['icon']) for g in H['guides'])+'</div>'
search='''<section id="search" class="search-box"><form onsubmit="return window.iwataSiteSearch(event)"><label for="site-search-input">困っていること・調べたい言葉から探す</label><div class="search-line"><input type="search" id="site-search-input" name="q" placeholder="例：住民票、学童、親の介護、ごみ"><button type="submit">探す</button></div></form><div class="search-examples"><a href="/?q=コンビニ交付休止#search">コンビニ交付休止</a><a href="/?q=学童#search">学童の申込み</a><a href="/?q=空き家#search">実家・空き家</a><a href="/?q=cohana#search">病児保育</a></div><div id="search-results" aria-live="polite"></div></section>'''
urgent='<section class="guide-section urgent-panel"><h2>急いでいるとき</h2><p>命に関わる緊急時は119番。救急車を呼ぶか迷うとき、受診先を探すときは次の案内へ。</p><div class="guide-grid">'+''.join(card(life(s),t,d,i) for s,t,d,i in [
('emergency/emergency-medical','救急車を呼ぶか迷う','119・#7119・#8000の使い分け','🚑'),('health-medical/holiday-night-emergency-care','夜間・休日の受診先','当番医・夜間救急室を確認','🏥'),('emergency/hazard-maps','避難先・災害リスク','住所から地図と避難情報を確認','🗺️')])+'</div></section>'
common=[('start-living/certificates','住民票・戸籍・印鑑','取得方法と休止日','📄'),('start-living/garbage-sorting-calendar','ごみの収集日・分別','地区のカレンダーを探す','🗑️'),('family-grow/nursery-childcare','保育園・一時預かり','希望年度と利用月から確認','👶'),('education/after-school-club','学童・放課後児童会','新規と継続の期限を確認','🎒'),('parents-care/care-started','親の介護','相談先と申請準備','👵'),('housing/vacant-house','空き家・解体補助','管理、相続、解体を分ける','🏠'),('work-life/national-health-insurance-tax','国民健康保険料','2026年度の仕組みと軽減','💴'),('start-living/water-start-stop-fees','水道の開始・中止','連絡先と受付時間','🚰')]
checks=[('start-living/moved-in','引っ越してきた','住所・水道・ごみ・保険','🧭'),('family-grow/marriage','結婚した','届出後の名義と住所変更','💍'),('family-grow/childbirth','子どもが生まれた','届出・手当・保険・健診','👶'),('work-life/nhk-pension','退職・転職した','健康保険と年金の切替え','💴'),('parents-care/care-started','介護が必要になった','主治医・家族・相談先','👵'),('end-of-life/bereavement-procedures','家族が亡くなった','急ぐ届出と後日の手続き','🕊️'),('moving-out/moving-away','浜松から転出する','転出・片付け・水道中止','📦')]
accordion=[]
for c in CAT:
 links=''.join(f'<li><a href="{esc(i["url"].replace(SITE,""))}">{esc(i["label"])}</a></li>' for i in c['items'])
 accordion.append(f'<details class="category" data-id="{c["id"]}"><summary><span class="topic-icon" aria-hidden="true">{c["emoji"]}</span><span class="card-text"><span class="card-title">{esc(c["title"])}</span><span class="card-desc">{esc(c["description"])}</span></span><span class="acc-arrow" aria-hidden="true"></span></summary><ul class="subitems">{links}<li class="subitems-more"><a href="{esc(c["url"].replace(SITE,""))}">この分野についてもっと詳しく見る</a></li></ul></details>')
home=f'''<section class="home-hero"><div class="home-hero-copy"><p class="eyebrow">浜松の暮らしを、ひとつずつ。</p><h1>浜松市の手続き・相談先を、<br>困りごとから探せます。</h1><p class="lead">住民票、ごみ、子育て、介護、住まい、防災。<br>何から始めるかを整理して、必要な公式情報へつなぎます。</p><p class="updated-date">{DISPLAY_DATE}更新 ｜ 中央区・浜名区・天竜区</p></div><figure class="home-hero-photo"><a href="https://hamamatsualb.atawi.link/features/hamamatsu-castle/?utm_source=hamamatsu_lifehack&amp;utm_medium=referral&amp;utm_campaign=local_gallery&amp;utm_content=castle_hero" data-track-click="home_photo_castle_hero" aria-label="浜松懐かし写真館で浜松城の昔の写真を見る"><img src="/assets/hamamatsu-castle-hero.webp" width="720" height="480" fetchpriority="high" decoding="async" alt="青空の下、石垣の上に建つ浜松城の天守と天守門"></a><figcaption><span>浜松城（中央区元城町）</span><a href="https://commons.wikimedia.org/wiki/File:Hamamatsu_Castle,_enkei-3.jpg">撮影 Saigen Jiro（CC0）</a></figcaption></figure></section>
{search}{urgent}<section class="guide-section"><h2>浜松で、何をしたいですか？</h2>{purpose}{HOME_PHOTOS}</section>
<section class="guide-section" id="latest"><h2>手続き前に確認したい、最新の案内</h2><p>{DISPLAY_DATE}に確認した受付日・変更点です。募集や予約の残枠は公式窓口で確認してください。</p>{news()}</section>
<section class="guide-section"><h2>よく使う手続き・相談</h2><div class="guide-grid compact">{''.join(card(life(s),t,d,i) for s,t,d,i in common)}</div></section>
<section class="guide-section"><h2>状況別チェックリスト</h2><p>確認した項目にチェックを付けられます。内容はこの端末のブラウザに保存されます。</p><div class="guide-grid compact">{''.join(card(life(s),t,d,i) for s,t,d,i in checks)}</div></section>
<section class="guide-section" id="category-links"><h2>暮らしの場面・目的から選ぶ</h2><p class="lead">13の分野から、必要な案内を開けます。<a href="/guides/">全{len(T)}ガイドを検索・絞り込み →</a></p><div class="category-accordion">{''.join(accordion)}</div></section>
<section class="guide-section"><h2>窓口は「区」と「手続き」で確認</h2><div class="local-area"><article><h3>中央区</h3><p>中央区役所のほか、東・西・南行政センターなど。用件によって担当窓口が異なります。</p></article><article><h3>浜名区</h3><p>浜名区役所・北行政センターなど。旧区名の案内を見たときは住所と担当を照合します。</p></article><article><h3>天竜区</h3><p>天竜区役所・各地域の窓口。訪問前に取扱業務と交通を確認してから出かけます。</p></article></div><p><a href="{life('start-living/city-hall-branches')}">窓口の場所・取扱業務を調べる →</a></p></section>
<section class="guide-section guide-note"><h2>情報の確認状況</h2><p>暮らしの案内は{len(T)}ページです。今回の確認は、年末年始の手続き・ごみ収集、保育施設の申込みなど、更新記録に記載した案内が対象です。</p><p>基礎情報の確認日と、今回の補足の確認日を分けて表示しています。<a href="/updates/">更新内容と確認範囲</a>をご覧ください。</p></section>
<section class="guide-section"><h2>運営者と編集方針</h2><p>富士ヶ丘サービス株式会社（代表 大石浩之）が運営する非公式の案内サイトです。行政の申請窓口と、運営会社の民間相談サービスを区別して掲載します。</p><p><a href="/about/">運営者・編集方針</a> ／ <a href="/terms/">利用条件</a></p></section>
<!-- PART:community-links:START --><!-- PART:community-links:END -->'''
write('/','浜松市の手続き・子育て・介護・空き家を困りごとから探す','浜松市の最新の手続き案内、子育て、介護、空き家、ごみ、移住を目的別に整理。出典と確認日、状況別チェックリストから必要な情報へ。',home,True)
for g in H['guides']:
 body=f'<p class="breadcrumb"><a href="/">トップ</a> ／ <a href="/guides/">ガイド</a></p><p class="eyebrow">目的から選ぶ</p><h1><span aria-hidden="true">{g["icon"]}</span> {esc(g["title"])}</h1><p class="lead">{esc(g["lead"])}</p>'
 for s in g['sections']:
  body+=f'<section class="guide-section"><h2>{esc(s["title"])}</h2><p>{esc(s["body"])}</p><ul class="source-links">'+''.join(f'<li><a href="{life(p)}">{esc(t)}</a></li>' for p,t in s['links'])+'</ul></section>'
  if g['slug']=='visit' and s['title']=='文化・学びを楽しむ':
   body+=VISIT_PHOTOS
 guide_date = DISPLAY_DATE if g['slug']=='visit' else '2026年11月18日'
 body+=f'<p class="guide-note">{guide_date}編集。手続きの条件・受付状況・出典はリンク先の各ガイドで確認できます。施設の予約や行政申請をこのサイトで受け付けるものではありません。</p>'
 write('/guides/'+g['slug']+'/',g['title'],g['description'],body)

options=''.join(f'<option>{esc(c)}</option>' for c in dict.fromkeys(x['category'] for x in T))
rows=[]
for t in T:
 query=' '.join([t['title'],t['category'],*t.get('synonyms',[])])
 rows.append(f'<li data-category="{esc(t["category"])}" data-search="{esc(query)}"><a href="{t["href"]}"><span aria-hidden="true">{t["icon"]}</span> {esc(t["title"])}</a><small>{esc(t["category"])}</small></li>')
body=f'<h1>浜松の暮らし・手続き 全{len(T)}ガイド</h1><p class="lead">目的から選ぶか、言葉と分野で絞り込めます。</p>{purpose}<section class="guide-section"><h2>すべてのガイドから探す</h2><div class="directory-controls"><label>言葉で探す<input type="search" id="directory-query" placeholder="例：ごみ、親、保育園"></label><label>分野<select id="directory-category"><option value="">すべての分野</option>{options}</select></label><button class="directory-clear" type="button">解除</button></div><p id="directory-count" aria-live="polite"></p><p id="directory-empty" hidden>一致するガイドがありません。言葉を短くするか、絞り込みを解除してください。</p><ul class="directory-list">{"".join(rows)}</ul></section>'
write('/guides/','浜松の暮らし・手続き 全ガイド','全分野のガイドを言葉とカテゴリで絞り込んで探せます。',body)
supp=[t for t in T if t.get('supplement_checked_date')]
body=f'<h1>確認した最新情報・更新記録</h1><p class="lead">確認日：{DISPLAY_DATE}。浜松市の公式情報から、今後の日程と終了した案内を分けて掲載します。</p><h2>これから確認したい案内</h2>{news()}<h2>終了した案内</h2>{news(archive=True)}<h2>今回の確認範囲</h2><p>年末年始の証明書・ごみ、12月の旅券手続き、2027年4月の認可保育施設、省エネエアコン補助、家康公祭りの開催案内を更新しました。下の一覧には、以前の確認分も含まれます。受付残枠や個別の申請可否は公式窓口でご確認ください。</p><p>終了日を過ぎた案内は「案内期間終了・記録」と表示します。これは日付による表示で、公式から自動取得した受付状況ではありません。新しい募集日程を推定して掲載することはありません。</p><h2>補足したページ</h2><ul class="source-links">'+''.join(f'<li><a href="{t["href"]}#guide-update">{esc(t["title"])}</a></li>' for t in supp)+'</ul><h2>市の新着を直接確認</h2><ul class="source-links"><li><a href="https://www.city.hamamatsu.shizuoka.jp/kurashi-tetsuzuki/oshirase.html">手続き・くらしのお知らせ</a></li><li><a href="https://www.city.hamamatsu.shizuoka.jp/kenko/oshirase.html">健康・医療・福祉のお知らせ</a></li><li><a href="https://www.city.hamamatsu.shizuoka.jp/">浜松市公式サイト</a></li></ul>'
write('/updates/','確認した最新情報・更新記録',f'{DISPLAY_DATE}に確認した浜松の手続き・子育て・補助金・催しの変更点と出典への案内。',body)
body='''<h1>運営者・編集方針</h1><p class="lead">浜松市の制度を、暮らしの困りごとから探しやすくする非公式の案内サイトです。</p><h2>運営者</h2><p>富士ヶ丘サービス株式会社／代表 大石浩之。行政機関ではありません。会社情報は<a href="https://www.fujigaoka-service.co.jp/">運営会社の公式サイト</a>をご覧ください。</p><h2>情報をまとめるときの方針</h2><ul><li>市・県・国、施設や交通事業者などの一次情報を優先し、各ページに確認先を掲載します。</li><li>日付・費用・対象者は年度や制度ごとに区別します。確認できないことを推測で確定しません。</li><li>既存の基礎情報と新しい補足は、確認日と範囲を分けます。個別の申請可否や医療・法律・税務の専門判断は担当窓口へ確認してください。</li><li>申込み・診療・予約を代行するサイトではありません。公式情報への案内です。</li></ul><h2>民間サービスの案内</h2><p>運営会社の不動産・介護相談へのリンクは民間サービスです。利用は任意であり、行政の制度や申請の可否に影響しません。救急・避難の入口には営業案内を配置しません。</p><h2>チェックリストの保存</h2><p>チェック状態は端末のブラウザ内に保存します。チェック内容を行政や運営会社へ送信する機能はありません。共用端末では利用後にリセットしてください。</p><h2>誤り・古い情報に気付いたとき</h2><p>対象ページのURLと、誤りと思われる内容・公式の根拠を添え、<a href="https://www.fujigaoka-service.co.jp/">運営会社の問い合わせ窓口</a>へお知らせください。行政申請や救急相談は各公式窓口へ直接ご連絡ください。</p><p><a href="/terms/">利用条件</a> ／ <a href="/updates/">更新記録</a></p>'''
write('/about/','運営者・編集方針','浜松ライフハックの運営者、出典確認、確認日の考え方、民間サービスと公式手続きの区別。',body)
print('Built home, directory, 3 purpose guides, updates and about')
