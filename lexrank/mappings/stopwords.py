import gzip
import json

from lexrank import settings

file = settings.ASSETS_ROOT / 'stopwords.json.gz'

with gzip.open(file, mode='rt', encoding='utf-8') as fp:
    _STOPWORDS = json.load(fp)

STOPWORDS = {}

for lang, stopwords in _STOPWORDS.items():
    STOPWORDS[lang] = set(stopwords)
