#!/usr/bin/env python3
"""
Batch scrape features text from legacy thinksrs.com pages.
Extracts text between the Features section and Specifications section.
Outputs to stdout for review.
"""

import re
import urllib.request
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).parent.parent

LEGACY_URLS = {
    'cg635': 'cg635', 'cg792': 'cg792', 'ctc100': 'ctc100', 'db64': 'db64',
    'dc215': 'dc215', 'dc205': 'dc205', 'ec301': 'ec301', 'ldc501': 'ldc501',
    'perf10': 'perf10', 'ps300': 'ps300', 'ptc10': 'ptc10',
    'qcm200': 'qcm200', 'qms100': 'qms', 'sg382': 'sg380', 'sg392': 'sg390',
    'sim900': 'sim900', 'sim910': 'sim910', 'sim918': 'sim918',
    'sim921': 'sim921', 'sim922': 'sim922923', 'sim928': 'sim928',
    'sim940': 'sim940', 'sim960': 'sim960', 'sim964': 'sim964',
    'sim970': 'sim970', 'sim985': 'sim983',
    'sr470': 'sr470474', 'sr620': 'sr620', 'sr625': 'sr625',
    'sr715': 'sr715720', 'sr770': 'sr760770',
    'sr250': 'sr250', 'sr400': 'sr400', 'sr540': 'sr540', 'sr542': 'sr542',
    'sr630': 'sr630', 'sc10': 'sc10', 'fs725': 'fs725', 'fs740': 'fs740',
    'fs752': 'fs752', 'fs710': 'fs710', 'prs10': 'prs10',
    'cs580': 'cs580', 'dg535': 'dg535', 'dg645': 'dg645',
    'ds345': 'ds345', 'ds360': 'ds360',
    'mpa100': 'mpa', 'mpa160': 'mpa160',
    'nl100': 'nl100', 'ugapm': 'ugapm', 'uga120': 'uga',
    'sr10': 'switchers', 'sr445a': 'sr445a', 'sr446': 'sr446',
    'sr550': 'preamp', 'sr554': 'sr554', 'sr555': 'sr555',
}


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = False

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)

    def get_text(self):
        return ' '.join(self.text)


def get_features_word_count(url):
    """Fetch page and estimate features section word count."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')

        parser = TextExtractor()
        parser.feed(html)
        text = parser.get_text()

        # Find features section
        feat_start = text.find('Features')
        spec_start = text.find('Specifications', feat_start + 10 if feat_start > 0 else 0)

        if feat_start > 0 and spec_start > feat_start:
            features = text[feat_start:spec_start]
            words = len(features.split())
            return words
        return 0
    except Exception as e:
        return -1


def main():
    import yaml

    # Check which products have short descriptions
    short_products = []
    for md in sorted(Path(ROOT / 'products').glob('*.md')):
        text = md.read_text(encoding='utf-8')
        m = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
        if not m:
            continue
        body = m.group(2).strip()
        words = len(body.split())
        sections = len(re.findall(r'^###', body, re.MULTILINE))
        slug = md.stem
        if words < 150 and slug in LEGACY_URLS:
            short_products.append((slug, words))

    print(f"Found {len(short_products)} products with short descriptions\n")

    for slug, local_words in short_products:
        url_part = LEGACY_URLS[slug]
        url = f'https://thinksrs.com/products/{url_part}'
        if not url.endswith('.html'):
            url += '.html'

        legacy_words = get_features_word_count(url)
        if legacy_words > local_words * 2:
            print(f"{slug:12s}  local={local_words:4d}w  legacy~{legacy_words:4d}w  ** NEEDS UPDATE **  {url}")
        elif legacy_words > 0:
            print(f"{slug:12s}  local={local_words:4d}w  legacy~{legacy_words:4d}w  (similar)")
        else:
            print(f"{slug:12s}  local={local_words:4d}w  legacy=???  (fetch failed or no features section)")


if __name__ == '__main__':
    main()
