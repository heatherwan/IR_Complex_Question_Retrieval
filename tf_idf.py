# -*- coding: utf-8 -*-
__author__ = 'Duc Tai Ly'
import math
import numpy as np
from utils import Utils


class TFIDF:
    """
    Class that calculates the tf-idf matrix with given term-doc matrix.
    Implementation based on dense vectors.
    """

    def __init__(self, documents):
        """

        :param documents: Should be a document-word count dict
        """
        if documents is None:
            raise Exception('TFIDF should be initialized with a corpus.')
        self.documents = documents
        self.idf_vector = {}
        self.term_doc_matrix = self.create_tf_idf_matrix()

    @staticmethod
    def get_max_freq_term(matrix, doc_id):
        """

        :param matrix: The term-doc matrix
        :param doc_id: The document od.
        :return: Returns the highest max. occurrence of all words in a document of given doc id.
        """
        max_freq = 0
        for k, v in matrix[doc_id].items():
            if v > max_freq:
                max_freq = v
        return max_freq

    # matrix: contains matrix of docs with terms and term frequency (corpus)
    # create idf vector
    @staticmethod
    def create_idf_matrix(matrix):
        """

        :param matrix: The term-doc matrix
        :return: Returns the idf-vector as dict {term: idf-weight}
        """
        idf_matrix = {}
        num_docs = len(matrix.items())
        vocabulary = set()
        for doc, terms in matrix.items():
            words_set = set(terms.keys())
            vocabulary = vocabulary.union(words_set)

        for term in vocabulary:
            for doc, terms in matrix.items():
                if term not in idf_matrix and term in terms:
                    idf_matrix.update({term: 1})
                elif term in terms:
                    count = idf_matrix[term]
                    idf_matrix.update({term: count+1})
        for word in idf_matrix:
            idf_matrix[word] = math.log(num_docs/idf_matrix[word], 10)
        return idf_matrix

    @staticmethod
    def create_tf_matrix(matrix):
        """

        Implementation like in slides Lecture 4 p.14
        tf(t,d) = (1 + log10(ft,d)) / (1 + log10 (max{ft’,d : t’ ∈ d}))
        :param matrix:
        :return:
        """
        tf_matrix = {}
        for k, v in matrix.items():
            max_freq = TFIDF.get_max_freq_term(matrix, k)
            for word in v:
                counter = 1+math.log(v[word], 10)
                denominator = 1+math.log(max_freq, 10)
                value = counter/denominator
                Utils.add_ele_to_matrix(tf_matrix, k, word, value)
        return tf_matrix

    def create_tf_idf_matrix(self):
        """
        Creates a tf-idf matrix.
        :return: It is a dict containing {docid: {term_1: tfidf-value, term_2: tfidf-value, ...}, ...}
        """
        matrix = self.documents
        # create the idf vector and the tf matrices
        self.idf_vector = self.create_idf_matrix(matrix)
        tf_matrix = TFIDF.create_tf_matrix(matrix)
        # based on the tf_matrix and idf_vector, we calculate the tf_idf_matrix
        tf_idf_matrix = {}
        for k, v in tf_matrix.items():
            for word in v:
                value = v[word] * self.idf_vector[word]
                Utils.add_ele_to_matrix(tf_idf_matrix, k, word, value)
        return tf_idf_matrix

    def create_query_vector(self, query):
        """
        creates a query vector with tf-idf values based on given document corpus.
        :param query: list of query strings.
        :return: tf-idf vector as dict.
        """
        tokens = query.split()
        tokens_set = set(tokens)
        word_dict = dict.fromkeys(tokens_set, 0)
        for word in tokens:
            word_dict[word] += 1
        for k, v in word_dict.items():
            try:
                word_dict[k] = self.idf_vector[k] * v
            except KeyError:
                # KeyError only when term is not in idf vector
                # thus, ignore the term by removing from query
                word_dict.pop(k)
        return word_dict