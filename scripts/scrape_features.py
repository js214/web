#!/usr/bin/env python3
"""
Scrape features text from legacy pages for products with short descriptions.
Run manually, review output, then paste into .md files.

Usage: python scripts/scrape_features.py <slug> [slug2 ...]
"""

import sys
import urllib.request
import re
from pathlib import Path

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
    'sr10': 'sr10_11_12', 'sr445a': 'sr445a', 'sr446': 'sr446',
    'sr550': 'sr550', 'sr554': 'sr554', 'sr555': 'sr555',
    'mpa100': 'mpa.html', 'mpa160': 'mpa160',
    'nl100': 'nl100', 'ugapm': 'ugapm', 'uga120': 'uga',
}

if __name__ == '__main__':
    slugs = sys.argv[1:] if len(sys.argv) > 1 else sorted(LEGACY_URLS.keys())

    for slug in slugs:
        url_part = LEGACY_URLS.get(slug)
        if not url_part:
            print(f'{slug}: no legacy URL mapped')
            continue

        url = f'https://thinksrs.com/products/{url_part}'
        if not url.endswith('.html'):
            url += '.html'

        print(f'\n=== {slug} ({url}) ===')
        # Just print the URL for manual WebFetch
        print(f'WebFetch URL: {url}')
