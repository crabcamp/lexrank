import numpy as np

from lexrank.algorithms.lexrank import LexRank


def test_lexrank():
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

    d5_s2 = 'n a gathering with the press held at the Prime Minister’s ' \
        'office, Blair contended that the crisis with Iraq “will not end ' \
        'until Iraq has absolutely and unconditionally respected its ' \
        'commitments” towards the United Nations.'

    d5_s3 = 'A spokesman for Tony Blair had indicated that the British ' \
        'Prime Minister gave permission to British Air Force Tornado planes ' \
        'stationed in Kuwait to join the aerial bombardment against Iraq.'

    documents = [
        [d1_s1],
        [d2_s1, d2_s2],
        [d2_s3],
        [d3_s1, d3_s2, d3_s3],
        [d4_s1],
        [d5_s1, d5_s2, d5_s3],
    ]

    sentences = []

    for doc in documents:
        sentences.extend(doc)

    lexrank = LexRank(documents, stopwords=set(), keep_numbers=True)

    tf_scores = [
        lexrank.calculate_tf(lexrank.tokenize_sentence(sentence))
        for sentence in sentences
    ]

    similarity_matrix = np.round(
        lexrank.calculate_similarity_matrix(tf_scores), 2,
    )

    expected_similarity_matrix = np.array([
        [1.00, 0.18, 0.03, 0.02, 0.00, 0.02, 0.01, 0.20, 0.03, 0.01, 0.00],
        [0.18, 1.00, 0.30, 0.08, 0.01, 0.02, 0.02, 0.03, 0.01, 0.01, 0.01],
        [0.03, 0.30, 1.00, 0.06, 0.01, 0.01, 0.02, 0.04, 0.01, 0.02, 0.01],
        [0.02, 0.08, 0.06, 1.00, 0.05, 0.06, 0.20, 0.06, 0.06, 0.05, 0.03],
        [0.00, 0.01, 0.01, 0.05, 1.00, 0.34, 0.08, 0.04, 0.04, 0.03, 0.07],
        [0.02, 0.02, 0.01, 0.06, 0.34, 1.00, 0.08, 0.03, 0.07, 0.08, 0.05],
        [0.01, 0.02, 0.02, 0.20, 0.08, 0.08, 1.00, 0.04, 0.00, 0.01, 0.00],
        [0.20, 0.03, 0.04, 0.06, 0.04, 0.03, 0.04, 1.00, 0.04, 0.04, 0.04],
        [0.03, 0.01, 0.01, 0.06, 0.04, 0.07, 0.00, 0.04, 1.00, 0.20, 0.24],
        [0.01, 0.01, 0.02, 0.05, 0.03, 0.08, 0.01, 0.04, 0.20, 1.00, 0.09],
        [0.00, 0.01, 0.01, 0.03, 0.07, 0.05, 0.00, 0.04, 0.24, 0.09, 1.00],
    ])

    assert np.array_equal(similarity_matrix, expected_similarity_matrix)
