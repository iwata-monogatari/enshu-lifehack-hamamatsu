"""Links from the Hamamatsu guides to the local photo archive."""
from html import escape
from urllib.parse import urlencode

ARCHIVE = 'https://hamamatsualb.atawi.link/features/'
FEATURES = {
    'hamamatsu-station': '昔の浜松駅・鍛冶町',
    'hamana-lake': '浜名湖・弁天島の昔の写真',
    'hamamatsu-festival': '浜松まつりの凧揚げ・御殿屋台',
    'tenryu-railway': '天竜二俣駅・佐久間の鉄道写真',
    'hamamatsu-aerial': '1946年からの浜松の空中写真',
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
        url = escape(f'{ARCHIVE}{slug}/?{query}', quote=True)
        links.append(f'<li><a href="{url}" data-track-click="{source}">{escape(FEATURES[slug])}</a></li>')
    return '<ul class="source-links">' + ''.join(links) + '</ul>'


HOME_PHOTOS = (
    '<div class="guide-note"><p>浜松懐かし写真館で、昔の浜松を写真で見る</p>'
    + photo_links('home_photo', ('hamamatsu-station', 'hamana-lake', 'hamamatsu-festival'))
    + '</div>'
)
VISIT_PHOTOS = (
    '<section class="guide-section" id="local-photo-archive"><h2>出かける前に、昔の浜松を写真で見る</h2>'
    '<p>訪ねたい場所が決まったら、浜松懐かし写真館で同じ場所の昔の風景を探せます。各写真に撮影時期と出典があります。</p>'
    + photo_links('visit_photo')
    + '</section>'
)
TOPIC_PHOTOS = {
    '/life/living-soon/transportation/': (
        '<section class="guide-update" id="local-photo-archive"><h2>昔の浜松駅と天竜の鉄道</h2>'
        '<p>浜松駅前のバスターミナルや、天竜二俣駅の駅舎・車両を昔の写真で見られます。</p>'
        + photo_links('transport_photo', ('hamamatsu-station', 'tenryu-railway'))
        + '</section>'
    ),
    '/life/play-out/cultural-facilities/': (
        '<section class="guide-update" id="local-photo-archive"><h2>写真で調べる、浜松の祭りと街の記録</h2>'
        '<p>郷土資料を調べるときは、浜松まつりの写真や国土地理院の空中写真から、当時の風景もたどれます。</p>'
        + photo_links('culture_photo', ('hamamatsu-festival', 'hamamatsu-aerial'))
        + '</section>'
    ),
}
