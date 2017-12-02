import math

import numpy as np
import pytest

from lexrank.algorithms.summarizer import LexRank


def test_lexrank():
    with pytest.raises(ValueError):
        lexrank = LexRank([[]])

    lexrank = LexRank(
        [['Hello,'], ['World!']],
        include_new_words=False,
    )

    assert math.isclose(lexrank.idf_score['hello'], math.log(2))
    assert lexrank.idf_score['test'] == 0

    lexrank = LexRank(
        [['Hello,'], ['World!']],
        include_new_words=True,
    )

    assert math.isclose(lexrank.idf_score['world'], math.log(2))
    assert math.isclose(lexrank.idf_score['test'], math.log(3))

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

    lexrank = LexRank(documents, keep_numbers=True)

    tf_scores = [
        lexrank._calculate_tf(lexrank.tokenize_sentence(sentence))
        for sentence in sentences
    ]

    similarity_matrix = np.round(
        lexrank._calculate_similarity_matrix(tf_scores), 2,
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

    lex_scores = lexrank.rank_sentences(
        sentences, normalize=True, discretize=True, threshold=.01)
    expexted_lex_scores = [
        0.55, 0.82, 0.91, 1., 0.91, 0.91, 0.73, 1., 0.73, 0.91, 0.73,
    ]

    assert np.array_equal(np.round(lex_scores, 2), expexted_lex_scores)

    lex_scores = lexrank.rank_sentences(
        sentences, normalize=True, discretize=False)
    expexted_lex_scores = [
        0.78, 1., 0.91, 1., 0.91, 0.95, 0.83, 0.86, 0.9, 0.86, 0.84,
    ]

    assert np.array_equal(np.round(lex_scores, 2), expexted_lex_scores)

    summary = lexrank.get_summary(sentences, threshold=.01)
    assert summary == [d4_s1]

    with pytest.raises(ValueError):
        summary = lexrank.get_summary(sentences, summary_size=0)

    with pytest.raises(ValueError):
        summary = lexrank.get_summary(sentences, summary_size=5, threshold=1.8)
