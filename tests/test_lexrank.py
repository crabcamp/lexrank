import gzip

from lexrank import LexRank
from lexrank.mappings import STOPWORDS
from tests.settings import DATA_ROOT


def test_lexrank():
    documents = []
    documents_dir = DATA_ROOT / 'bbc_politics'
    document_files = documents_dir.files()

    for file in document_files:
        with gzip.open(file, mode='rt', encoding='utf-8') as fp:
            documents.append(fp.readlines())

    lexrank = LexRank(
        documents,
        stopwords=STOPWORDS['en'],
        keep_numbers=False,
        keep_emails=False,
        include_new_words=True,
    )

    sentences = [
        'One of David Cameron\'s closest friends and Conservative allies, '
        'George Osborne rose rapidly after becoming MP for Tatton in 2001.',

        'Michael Howard promoted him from shadow chief secretary to the '
        'Treasury to shadow chancellor in May 2005, at the age of 34.',

        'Mr Osborne took a key role in the election campaign and has been at '
        'the forefront of the debate on how to deal with the recession and '
        'the UK\'s spending deficit.',

        'Even before Mr Cameron became leader the two were being likened to '
        'Labour\'s Blair/Brown duo. The two have emulated them by becoming '
        'prime minister and chancellor, but will want to avoid the spats.',

        'Before entering Parliament, he was a special adviser in the '
        'agriculture department when the Tories were in government and later '
        'served as political secretary to William Hague.',

        'The BBC understands that as chancellor, Mr Osborne, along with the '
        'Treasury will retain responsibility for overseeing banks and '
        'financial regulation.',

        'Mr Osborne said the coalition government was planning to change the '
        'tax system \"to make it fairer for people on low and middle '
        'incomes\", and undertake \"long-term structural reform\" of the '
        'banking sector, education and the welfare state.',
    ]

    summary = lexrank.get_summary(sentences, discretize=False)
    assert summary == [sentences[5]]
