import argparse
import gzip
import json
import sys

from path import Path

from lexrank import settings
from lexrank.utils.text import clean_text


def assemble_stopwords(source_dir):
    files = source_dir.files('*.txt')
    stopwords_map = {}

    for file_path in files:
        lang = file_path.namebase
        lang_words = set()

        with file_path.open(mode='rt', encoding='utf-8') as fp:
            for name in fp.readlines():
                lang_words.add(clean_text(name))

        stopwords_map[lang] = list(lang_words)
        sys.stdout.write('  ' + lang + ' ' + 'stopwords collected\n')

    if not stopwords_map:
        return

    out_file = settings.ASSETS_ROOT / 'stopwords.json.gz'

    with gzip.open(out_file, mode='wt', encoding='utf-8') as fp:
        json.dump(stopwords_map, fp)

        msg = 'Stopwords written to {out_file}\n'.format(out_file=out_file)
        sys.stdout.write(msg)


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_dir', type=Path, required=True)

    return parser


def entrypoint():
    parser = setup_parser()
    options = parser.parse_args(sys.argv[1:])

    assemble_stopwords(options.source_dir)
