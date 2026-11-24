"""Link previews for Hamamatsu's entry points and frequently shared guides."""
from html import escape

TOPIC_PREVIEWS = {
    '/life/living-soon/transportation/',
    '/life/living-soon/about-hamamatsu/',
    '/life/play-out/cultural-facilities/',
    '/life/start-living/certificates/',
    '/life/start-living/garbage-sorting-calendar/',
    '/life/start-living/passport/',
    '/life/family-grow/nursery-childcare/',
}


def share_metadata(origin, path, title, description):
    alt = '浜松城の天守と天守門'
    properties = {
        'og:type': 'website',
        'og:site_name': '浜松ライフハック',
        'og:locale': 'ja_JP',
        'og:title': title,
        'og:description': description,
        'og:url': origin + path,
        'og:image': origin + '/assets/hamamatsu-castle-hero.webp',
        'og:image:type': 'image/webp',
        'og:image:width': '720',
        'og:image:height': '480',
        'og:image:alt': alt,
    }
    names = {
        'twitter:card': 'summary_large_image',
        'twitter:image:alt': alt,
        'robots': 'max-image-preview:large',
    }
    tags = [f'<meta property="{key}" content="{escape(value, quote=True)}">' for key, value in properties.items()]
    tags += [f'<meta name="{key}" content="{escape(value, quote=True)}">' for key, value in names.items()]
    return '\n'.join(tags)
