import gzip
import json
import sys

from colorama import Fore, Style

from lexrank import settings
from lexrank.utils.text import clean_text


def assemble_stopwords():
    source_dir = settings.ASSETS_ROOT / 'stopwords_raw'
    out_file = settings.ASSETS_ROOT / 'stopwords.json.gz'

    files = source_dir.files('*.txt')

    stopwords_map = dict()

    for file in files:
        lang = file.namebase
        lang_words = set()

        with file.open(mode='rt', encoding='utf-8') as fp:
            for name in fp.readlines():
                lang_words.add(clean_text(name))

        stopwords_map[lang] = list(lang_words)

        sys.stdout.write(Fore.GREEN + '  ' + lang + ' ' + Style.RESET_ALL)
        sys.stdout.write(Fore.CYAN + 'stopwords collected\n' + Style.RESET_ALL)

    with gzip.open(out_file, mode='wt', encoding='utf-8') as fp:
        json.dump(stopwords_map, fp)

        msg = 'Stopwords written to {out_file}\n'.format(out_file=out_file)
        sys.stdout.write(Style.BRIGHT + msg + Style.RESET_ALL)
