import math
from collections import defaultdict

import numpy as np

from lexrank.utils.text import tokenize


class LexRank():
    def __init__(
        self,
        documents,
        stopwords,
        similarity_threshold=.1,
        keep_numbers=False,
        keep_emails=False,
        include_new_words=True,
    ):
        self.stopwords = stopwords
        self.similarity_threshold = similarity_threshold
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
            raise ValueError('Documents are not informative.')

        self.bags_of_words = bags_of_words
        self.idf_score = self.calculate_idf()

    def tokenize_sentence(self, sentence):
        tokens = tokenize(
            sentence,
            self.stopwords,
            keep_numbers=self.keep_numbers,
            keep_emails=self.keep_emails,
        )
        return tokens

    def calculate_idf(self):
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

    def calculate_tf(self, tokenized_sentence):
        tf_score = dict()

        for word in set(tokenized_sentence):
            tf = tokenized_sentence.count(word)
            tf_score[word] = tf

        return tf_score

    def idf_modified_cosine(self, tf_scores, i, j):
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

    def calculate_similarity_matrix(self, tf_scores):
        length = len(tf_scores)

        similarity_matrix = np.zeros([length] * 2)

        for i in range(length):
            for j in range(i, length):
                similarity = self.idf_modified_cosine(tf_scores, i, j)

                if similarity:
                    similarity_matrix[i, j] = similarity
                    similarity_matrix[j, i] = similarity

        return similarity_matrix
