import math
from collections import defaultdict

import numpy as np

from lexrank.algorithms.power_method import stationary_distribution
from lexrank.utils.text import tokenize


class LexRank:
    def __init__(
        self,
        documents,
        stopwords=None,
        keep_numbers=False,
        keep_emails=False,
        include_new_words=True,
    ):
        if stopwords is None:
            self.stopwords = set()
        else:
            self.stopwords = stopwords

        self.keep_numbers = keep_numbers
        self.keep_emails = keep_emails
        self.include_new_words = include_new_words

        bags_of_words = []

        for doc in documents:
            doc_words = set()

            for sentence in doc:
                words = self.tokenize_sentence(sentence)
                doc_words.update(words)

            if doc_words:
                bags_of_words.append(doc_words)

        if not bags_of_words:
            raise ValueError('documents are not informative')

        self.bags_of_words = bags_of_words
        self.idf_score = self._calculate_idf()

    def tokenize_sentence(self, sentence):
        tokens = tokenize(
            sentence,
            self.stopwords,
            keep_numbers=self.keep_numbers,
            keep_emails=self.keep_emails,
        )

        return tokens

    def _calculate_idf(self):
        doc_number_total = len(self.bags_of_words)

        if self.include_new_words:
            default_value = math.log(doc_number_total + 1)

        else:
            default_value = 0

        idf_score = defaultdict(lambda: default_value)

        for word in set.union(*self.bags_of_words):
            doc_number_word = sum(1 for bag in self.bags_of_words if word in bag)  # noqa
            idf_score[word] = math.log(doc_number_total / doc_number_word)

        return idf_score

    def _calculate_tf(self, tokenized_sentence):
        tf_score = {}

        for word in set(tokenized_sentence):
            tf = tokenized_sentence.count(word)
            tf_score[word] = tf

        return tf_score

    def _idf_modified_cosine(self, tf_scores, i, j):
        if i == j:
            return 1

        tf_i, tf_j = tf_scores[i], tf_scores[j]
        words_i, words_j = set(tf_i.keys()), set(tf_j.keys())

        nominator = 0

        for word in words_i & words_j:
            idf = self.idf_score[word]
            nominator += tf_i[word] * tf_j[word] * idf ** 2

        if math.isclose(nominator, 0):
            return 0

        denominator_i, denominator_j = 0, 0

        for word in words_i:
            tfidf = tf_i[word] * self.idf_score[word]
            denominator_i += tfidf ** 2

        for word in words_j:
            tfidf = tf_j[word] * self.idf_score[word]
            denominator_j += tfidf ** 2

        similarity = nominator / math.sqrt(denominator_i * denominator_j)

        return similarity

    def _calculate_similarity_matrix(self, tf_scores):
        length = len(tf_scores)

        similarity_matrix = np.zeros([length] * 2)

        for i in range(length):
            for j in range(i, length):
                similarity = self._idf_modified_cosine(tf_scores, i, j)

                if similarity:
                    similarity_matrix[i, j] = similarity
                    similarity_matrix[j, i] = similarity

        return similarity_matrix

    def _markov_matrix_discrete(self, similarity_matrix, threshold):
        markov_matrix = np.zeros(similarity_matrix.shape)

        for i in range(len(similarity_matrix)):
            columns = np.where(similarity_matrix[i] > threshold)[0]  # noqa
            markov_matrix[i, columns] = 1 / len(columns)

        return markov_matrix

    def _markov_matrix(self, similarity_matrix):
        row_sum = similarity_matrix.sum(axis=1, keepdims=True)

        return similarity_matrix / row_sum

    def rank_sentences(
        self,
        sentences,
        threshold=.03,
        discretize=True,
        fast_power_method=True,
        normalize=False,
    ):
        if not isinstance(threshold, float) or not 0 <= threshold < 1:
            raise ValueError(
                '\'threshold\' should be a floating-point number '
                'from the interval [0, 1)',
            )

        tf_scores = [
            self._calculate_tf(self.tokenize_sentence(sentence))
            for sentence in sentences
        ]

        similarity_matrix = self._calculate_similarity_matrix(tf_scores)

        if discretize:
            markov_matrix = self._markov_matrix_discrete(
                similarity_matrix,
                threshold=threshold,
            )

        else:
            markov_matrix = self._markov_matrix(similarity_matrix)

        lexrank = stationary_distribution(
            markov_matrix,
            increase_power=fast_power_method,
        )

        if normalize:
            max_val = max(lexrank)
            lexrank = [val / max_val for val in lexrank]

        return lexrank

    def get_summary(
        self,
        sentences,
        summary_size=1,
        threshold=.03,
        discretize=True,
        fast_power_method=True,
    ):
        if not isinstance(summary_size, int) or summary_size < 1:
            raise ValueError('\'summary_size\' should be a positive integer')

        lexrank = self.rank_sentences(
            sentences,
            threshold=threshold,
            discretize=discretize,
            fast_power_method=fast_power_method,
        )

        sorted_ix = np.argsort(lexrank)[::-1]
        summary = [sentences[i] for i in sorted_ix[:summary_size]]

        return summary
