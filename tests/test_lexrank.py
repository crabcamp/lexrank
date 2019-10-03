import gzip
import math
from collections import Counter

import numpy as np
import pytest

from lexrank import LexRank
from lexrank.mappings.stopwords import STOPWORDS
from tests.settings import DATA_ROOT


def test_lexrank():
    with pytest.raises(ValueError):
        lxr = LexRank([[]])

    lxr = LexRank(
        [['Hello,'], ['World!']],
        include_new_words=False,
    )

    assert math.isclose(lxr.idf_score['hello'], math.log(2))
    assert lxr.idf_score['test'] == 0

    lxr = LexRank(
        [['Hello,'], ['World!']],
        include_new_words=True,
    )

    assert math.isclose(lxr.idf_score['world'], math.log(2))
    assert math.isclose(lxr.idf_score['test'], 1)

    d1_s1 = 'Iraqi Vice President Taha Yassin Ramadan announced today, ' \
        'Sunday, that Iraq refuses to back down from its decision to stop ' \
        'cooperating with disarmament inspectors before its demands are met.'

    d2_s1 = 'Iraqi Vice president Taha Yassin Ramadan announced today, ' \
        'Thursday, that Iraq rejects cooperating with the United Nations ' \
        'except on the issue of lifting the blockade imposed ' \
        'upon it since the year 1990.'

    d2_s2 = 'Ramadan told reporters in Baghdad that ”Iraq cannot deal ' \
        'positively with whoever represents the Security Council unless ' \
        'there was a clear stance on the issue of lifting the ' \
        'blockade off of it.'

    d2_s3 = 'Baghdad had decided late last October to completely cease ' \
        'cooperating with the inspectors of the United Nations Special ' \
        'Commission (UNSCOM), in charge of disarming Iraq’s weapons, and ' \
        'whose work became very limited since the fifth of August, ' \
        'and announced it will not resume its cooperation with the ' \
        'Commission even if it were subjected to a military operation.'

    d3_s1 = 'The Russian Foreign Minister, Igor Ivanov, warned today, ' \
        'Wednesday against using force against Iraq, which will destroy, ' \
        'according to him, seven years of difficult diplomatic work and ' \
        'will complicate the regional situation in the area.'

    d3_s2 = 'Ivanov contended that carrying out air strikes against Iraq, ' \
        'who refuses to cooperate with the United Nations inspectors, ' \
        '“will end the tremendous work achieved by the international group ' \
        'during the past seven years and will complicate the ' \
        'situation in the region.”'

    d3_s3 = 'Nevertheless, Ivanov stressed that Baghdad must resume working ' \
        'with the Special Commission in charge of disarming the Iraqi ' \
        'weapons of mass destruction (UNSCOM).'

    d4_s1 = 'The Special Representative of the United Nations ' \
        'Secretary-General in Baghdad, Prakash Shah, announced today, ' \
        'Wednesday, after meeting with the Iraqi Deputy Prime Minister ' \
        'Tariq Aziz, that Iraq refuses to back down from its decision to ' \
        'cut off cooperation with the disarmament inspectors.'

    d5_s1 = 'British Prime Minister Tony Blair said today, Sunday, that the ' \
        'crisis between the international community and Iraq “did not end” ' \
        'and that Britain is still “ready, prepared, and able to strike Iraq.”'

    d5_s2 = 'In a gathering with the press held at the Prime Minister’s ' \
        'office, Blair contended that the crisis with Iraq “will not end ' \
        'until Iraq has absolutely and unconditionally respected its ' \
        'commitments” towards the United Nations.'

    d5_s3 = 'A spokesman for Tony Blair had indicated that the British ' \
        'Prime Minister gave permission to British Air Force Tornado planes ' \
        'stationed in Kuwait to join the aerial bombardment against Iraq.'

    documents = [
        [d1_s1],
        [d2_s1, d2_s2, d2_s3],
        [d3_s1, d3_s2, d3_s3],
        [d4_s1],
        [d5_s1, d5_s2, d5_s3],
    ]

    sentences = []

    for doc in documents:
        sentences.extend(doc)

    lxr = LexRank(documents, keep_numbers=True)

    tf_scores = [
        Counter(lxr.tokenize_sentence(sentence)) for sentence in sentences
    ]

    similarity_matrix = np.round(
        lxr._calculate_similarity_matrix(tf_scores), 2,
    )

    expected_similarity_matrix = np.array([
        [1.00, 0.17, 0.02, 0.03, 0.00, 0.01, 0.00, 0.17, 0.03, 0.00, 0.00],
        [0.17, 1.00, 0.32, 0.19, 0.02, 0.03, 0.03, 0.04, 0.01, 0.02, 0.01],
        [0.02, 0.32, 1.00, 0.13, 0.02, 0.02, 0.05, 0.05, 0.01, 0.03, 0.02],
        [0.03, 0.19, 0.13, 1.00, 0.05, 0.05, 0.19, 0.06, 0.05, 0.06, 0.03],
        [0.00, 0.02, 0.02, 0.05, 1.00, 0.33, 0.09, 0.05, 0.03, 0.03, 0.06],
        [0.01, 0.03, 0.02, 0.05, 0.33, 1.00, 0.09, 0.04, 0.06, 0.08, 0.04],
        [0.00, 0.03, 0.05, 0.19, 0.09, 0.09, 1.00, 0.05, 0.01, 0.01, 0.01],
        [0.17, 0.04, 0.05, 0.06, 0.05, 0.04, 0.05, 1.00, 0.04, 0.05, 0.04],
        [0.03, 0.01, 0.01, 0.05, 0.03, 0.06, 0.01, 0.04, 1.00, 0.20, 0.24],
        [0.00, 0.02, 0.03, 0.06, 0.03, 0.08, 0.01, 0.05, 0.20, 1.00, 0.10],
        [0.00, 0.01, 0.02, 0.03, 0.06, 0.04, 0.01, 0.04, 0.24, 0.10, 1.00],
    ])

    assert np.array_equal(similarity_matrix, expected_similarity_matrix)

    lex_scores = lxr.rank_sentences(sentences, threshold=.01)
    expected_lex_scores = [
        0.65, 0.98, 1.09, 1.2, 1.09, 1.09, 0.87, 1.2, 0.87, 1.09, 0.87,
    ]

    assert np.array_equal(np.round(lex_scores, 2), expected_lex_scores)

    lex_scores = lxr.rank_sentences(sentences, threshold=None)
    expected_lex_scores = [
        0.87, 1.12, 1.02, 1.12, 1.02, 1.06, 0.93, 0.96, 1.01, 0.96, 0.94,
    ]

    assert np.array_equal(np.round(lex_scores, 2), expected_lex_scores)

    similarity = lxr.sentences_similarity(d1_s1, d2_s1)
    expected_similarity = 0.17278015602565383

    assert math.isclose(similarity, expected_similarity)

    summary = lxr.get_summary(sentences, threshold=.01)
    assert summary == [d4_s1]

    with pytest.raises(ValueError):
        summary = lxr.get_summary(sentences, summary_size=0)

    with pytest.raises(ValueError):
        summary = lxr.get_summary(sentences, summary_size=5, threshold=1.8)


def test_lexrank_bbc_news():
    documents = []
    documents_dir = DATA_ROOT / 'bbc_politics'
    document_files = documents_dir.files()

    for file_path in document_files:
        with gzip.open(file_path, mode='rt', encoding='utf-8') as fp:
            documents.append(fp.readlines())

    lxr = LexRank(
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

    summary = lxr.get_summary(sentences, threshold=None)
    assert summary == [sentences[5]]
