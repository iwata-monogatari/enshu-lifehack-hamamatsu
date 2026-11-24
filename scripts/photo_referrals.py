"""Links from the Hamamatsu guides to the local photo archive."""
from html import escape
from urllib.parse import urlencode

ARCHIVE = 'https://hamamatsualb.atawi.link/features/'
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
        '<p>浜松駅前のバスターミナル、遠鉄の赤電、天竜二俣駅の駅舎や車両を昔の写真で見られます。</p>'
        + photo_links('transport_photo', ('hamamatsu-station', 'entetsu-red-train', 'tenryu-railway'))
        + '</section>'
    ),
    '/life/play-out/cultural-facilities/': (
        '<section class="guide-update" id="local-photo-archive"><h2>写真で調べる、浜松の祭りと街の記録</h2>'
        '<p>郷土資料を調べるときは、浜松まつり、浜松城、昭和初期の街並みや空中写真から、当時の風景もたどれます。</p>'
        + photo_links('culture_photo', ('hamamatsu-festival', 'hamamatsu-castle', 'showa-hamamatsu', 'hamamatsu-aerial'))
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
        + photo_links('city_photo', ('showa-hamamatsu', 'matsubishi'))
        + '</section>'
    ),
}
