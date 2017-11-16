import gzip
import json

from pyrsistent import freeze

import settings

file = settings.ASSETS_ROOT / 'stopwords.json.gz'

with gzip.open(file, mode='rt', encoding='utf-8') as fp:
    _STOPWORDS = json.load(fp)

STOPWORDS = dict()

for lang, stopwords in _STOPWORDS.items():
    STOPWORDS[lang] = set(stopwords)

STOPWORDS = freeze(STOPWORDS)
