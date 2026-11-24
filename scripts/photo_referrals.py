"""Links from the Hamamatsu guides to the local photo archive."""
from html import escape
from urllib.parse import urlencode

ARCHIVE = 'https://hamamatsualb.atawi.link'
FEATURES = {
    'hamamatsu-station': '昔の浜松駅・鍛冶町',
    'hamana-lake': '浜名湖・弁天島の昔の写真',
    'hamamatsu-festival': '浜松まつりの凧揚げ・御殿屋台',
    'tenryu-railway': '天竜二俣駅・佐久間の鉄道写真',
    'matsubishi': '松菱百貨店・鍛冶町の昔の写真',
    'entetsu-red-train': '遠州鉄道・赤電の昔の写真',
    'showa-hamamatsu': '昭和初期の広小路・田町・馬込橋',
    'hamamatsu-castle': '浜松城の城跡と昔の天守の写真',
    'hamamatsu-aerial': '1946年からの浜松の空中写真',
    'hamamatsu-engine-depot-1949': '昭和24年の浜松機関区',
    'hamamatsu-festival-shops-1952': '昭和27年刊の浜松まつりと商店',
    'hamamatsu-city-guide-1960': '昭和35年度の市勢要覧に残る浜松の暮らし',
}

PHOTO_PAGES = {
    'commons-62343336': '五社公園にあった浜松市立図書館',
    'commons-1454485': '松城町の浜松市立中央図書館',
    'commons-50470038': '中央図書館2階の学習室',
    'commons-50470039': '中央図書館の郷土資料室',
    'commons-61227609': '城北図書館のグループ学習室',
    'official-ct00000083-dg00000088-028-crop01': '昭和35年度の市勢要覧に載る市立図書館',
    'commons-1453987': '浜松市楽器博物館の写真',
    'commons-196363': 'アクトシティ浜松の写真',
    'commons-6677130': '浜北総合体育館・グリーンアリーナの写真',
    'commons-7071945': '浜松アリーナの写真',
    'commons-85204558': '水窪総合体育館の写真',
    'commons-6736809': '浜松市総合水泳場ToBiOの写真',
    'commons-23206485': '弁天島海浜公園の入口',
    'commons-57767994': '佐鳴湖公園の噴水池',
    'commons-5944155': 'はままつフラワーパークの噴水',
    'commons-128725310': '可美公園の広場',
    'commons-56676146': '浜松城公園の入口',
    'bus-terminal-2001': '平成13年の浜松駅バスターミナル',
    'bentenjima-station-2008': '平成20年の弁天島駅',
    'official-100162-postcard162_005': '浜松追分尋常小学校の教室設備',
    'official-ct00000083-dg00000088-031-crop02': '昭和35年度の市勢要覧に載る教室風景',
}


def photo_links(placement, slugs=FEATURES):
    links = []
    for slug in slugs:
        source = placement + '_' + slug
        query = urlencode({
            'utm_source': 'hamamatsu_lifehack',
            'utm_medium': 'referral',
            'utm_campaign': 'local_gallery',
            'utm_content': source,
        })
        if slug == 'library':
            path, label = '/library/', '浜松の古写真・地域資料を調べる'
        elif slug in FEATURES:
            path, label = f'/features/{slug}/', FEATURES[slug]
        else:
            path, label = f'/photos/{slug}/', PHOTO_PAGES[slug]
        url = escape(f'{ARCHIVE}{path}?{query}', quote=True)
        links.append(f'<li><a href="{url}" data-track-click="{source}">{escape(label)}</a></li>')
    return '<ul class="source-links">' + ''.join(links) + '</ul>'


def archive_section(placement, heading, description, keys):
    return (
        '<section class="guide-update" id="local-photo-archive">'
        f'<h2>{escape(heading)}</h2><p>{escape(description)}</p>'
        + photo_links(placement, keys)
        + '</section>'
    )


HOME_PHOTOS = (
    '<div class="guide-note"><p>浜松懐かし写真館で、昔の浜松を写真で見る</p>'
    + photo_links('home_photo', ('hamamatsu-station', 'hamana-lake', 'hamamatsu-festival', 'hamamatsu-city-guide-1960'))
    + '</div>'
)
VISIT_PHOTOS = (
    '<section class="guide-section" id="local-photo-archive"><h2>出かける前に、昔の浜松を写真で見る</h2>'
    '<p>訪ねたい場所が決まったら、浜松懐かし写真館で同じ場所の昔の風景を探せます。各写真に撮影時期と出典があります。</p>'
    + photo_links('visit_photo', (key for key in FEATURES if key != 'hamamatsu-castle'))
    + '</section>'
)
TOPIC_PHOTOS = {
    '/life/living-soon/transportation/': (
        '<section class="guide-update" id="local-photo-archive"><h2>昔の浜松駅と天竜の鉄道</h2>'
        '<p>浜松駅前のバスターミナル、遠鉄の赤電、天竜二俣駅の駅舎や車両を昔の写真で見られます。</p>'
        + photo_links('transport_photo', ('hamamatsu-station', 'entetsu-red-train', 'tenryu-railway', 'hamamatsu-engine-depot-1949'))
        + '</section>'
    ),
    '/life/play-out/cultural-facilities/': (
        '<section class="guide-update" id="local-photo-archive"><h2>写真で調べる、浜松の祭りと街の記録</h2>'
        '<p>郷土資料を調べるときは、浜松まつり、浜松城、昭和初期の街並みや空中写真から、当時の風景もたどれます。</p>'
        + photo_links('culture_photo', ('commons-1453987', 'commons-196363', 'hamamatsu-festival', 'hamamatsu-castle', 'showa-hamamatsu', 'hamamatsu-aerial', 'hamamatsu-festival-shops-1952'))
        + '</section>'
    ),
    '/life/play-out/ieyasu-festival-2026/': (
        '<section class="guide-update" id="local-photo-archive"><h2>会場の浜松城公園を古写真でたどる</h2>'
        '<p>浜松城公園周辺の移り変わりを、城跡の絵葉書と天守の写真で見られます。</p>'
        + photo_links('ieyasu_photo', ('hamamatsu-castle',))
        + '</section>'
    ),
    '/life/living-soon/about-hamamatsu/': (
        '<section class="guide-update" id="local-photo-archive"><h2>浜松の街を昔の写真で知る</h2>'
        '<p>広小路や田町の通り、鍛冶町の松菱百貨店。浜松の街なかを古写真でたどれます。</p>'
        + photo_links('city_photo', ('showa-hamamatsu', 'matsubishi', 'hamamatsu-city-guide-1960', 'hamamatsu-aerial'))
        + '</section>'
    ),
    '/life/play-out/visit-library/': archive_section(
        'library_photo', '図書館の郷土資料と昔の浜松を調べる',
        '中央図書館の郷土資料室や昔の市立図書館を写真で見られます。地域の調べ物には、街並み・空中写真の特集から各写真の原資料へ進めます。',
        ('commons-50470039','commons-62343336','official-ct00000083-dg00000088-028-crop01','showa-hamamatsu','hamamatsu-aerial','library'),
    ),
    '/life/play-out/facilities-library-parks/': archive_section(
        'facility_photo', '訪ねる施設の外観を写真で見る',
        '図書館・博物館・体育館・公園の入口や建物を見て、出かける場所の目印を確認できます。撮影時期は写真ごとにご確認ください。',
        ('commons-1454485','commons-1453987','commons-6677130','commons-56676146'),
    ),
    '/life/play-out/find-parks/': archive_section(
        'parks_photo', '公園の風景を写真で見比べる',
        '浜松城公園の天守、弁天島の湖岸、佐鳴湖公園の庭園、舘山寺のフラワーパークを写真で見られます。',
        ('hamamatsu-castle','commons-23206485','commons-57767994','commons-5944155'),
    ),
    '/life/play-out/parking-access/': archive_section(
        'access_photo', '浜松駅・弁天島の到着地点を写真で見る',
        '浜松駅のバスターミナルや弁天島駅、海浜公園の入口を写した記録です。現在の乗り場と駐車場は、上の案内先で確認できます。',
        ('bus-terminal-2001','bentenjima-station-2008','commons-23206485'),
    ),
    '/life/play-out/kids-playgrounds/': archive_section(
        'family_park_photo', '子どもと歩ける公園を写真で見る',
        '可美公園の広場と佐鳴湖公園のサンクンガーデンを写真で見られます。広場や園内を散歩する先を選ぶ手掛かりになります。',
        ('commons-128725310','commons-57767994'),
    ),
    '/life/education/study-facilities/': archive_section(
        'study_photo', '図書館の学習室・学習席を写真で見る',
        '中央図書館と城北図書館の学習スペースを写した写真です。現在の席の使い方・予約は上の利用案内で確認できます。',
        ('commons-50470038','commons-61227609'),
    ),
    '/life/education/elementary-middle-school/': archive_section(
        'school_photo', '浜松の昔の教室を見る',
        '昔の机や教室設備を写した絵葉書と、昭和の市勢要覧に収録された学校の写真です。浜松の学校の歩みを知る資料として見られます。',
        ('official-100162-postcard162_005','official-ct00000083-dg00000088-031-crop02'),
    ),
    '/life/play-out/sports-facilities/': archive_section(
        'sport_photo', '浜松の体育館の外観を写真で見る',
        '浜松アリーナ、浜北のグリーンアリーナ、水窪総合体育館の写真です。訪ねる施設の建物を確認できます。',
        ('commons-7071945','commons-6677130','commons-85204558'),
    ),
    '/life/play-out/swimming-pools/': archive_section(
        'pool_photo', '浜松市総合水泳場ToBiOの建物を見る',
        '施設の外観を写真で確認できます。営業日や利用時間は上の公式案内をご確認ください。',
        ('commons-6736809',),
    ),
}
