# -*- coding: utf-8 -*-
import math
__author__ = 'Duc Tai Ly'


class BM25:

    # documents: is a dict of doc_ids containing terms with corresponding weights
    # e.g. {'id_1': {'term1': value1, 'term2': value2, ... }, 'id_2': {'term12': value12, 'term2': value22, ... }, ...}
    # default: k = 1.2, k is best in [1.2, 2.0]
    # default: b = 0.75, b is best in [0.5, 0.8]
    # see: https://www.researchgate.net/publication/220613776_The_Probabilistic_Relevance_Framework_BM25_and_Beyond
    def __init__(self, documents, b=None, k=None):
        self.documents = documents
        if b is None:
            self.b = 0.75
        else:
            self.b = b
        if k is None:
            self.k = 1.2
        else:
            self.k = k

    # documents average length
    def get_average_doc_length(self):
        num_docs = len(self.documents.keys())
        num_items = 0
        for k, v in self.documents.items():
            num_items = num_items + len(v)
        return num_items/num_docs

    # document exact length of specified doc_id
    def get_doc_length(self, doc_id):
        doc_len = 0
        for term, value in self.documents[doc_id].items():
            doc_len += value
        return doc_len

    # get frequency of term in document with doc_id
    def get_term_frequency_in_doc(self, term, doc_id):
        try:
            return self.documents[doc_id][term]
        except KeyError:
            return 0

    # get weight of term as idf weight
    # log10(#docs/df)
    def idf_weight(self, term):
        df = 0
        num_docs = len(self.documents.keys())
        for k, v in self.documents.items():
            if self.get_term_frequency_in_doc(term, k) > 0:
                df = df + 1
        if df != 0:
            return math.log(num_docs/df, 10)
        else:
            return 0

    # get weight based on article
    # https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables
    def idf_weight_2(self, term):
        df = 0
        num_docs = len(self.documents.keys())
        for k, v in self.documents.items():
            if self.get_term_frequency_in_doc(term, k) > 0:
                df = df + 1
        idf = math.log1p(1 + (num_docs - df + 0.5)/(df + 0.5))
        return idf

    # calculate relevance score of query and corresponding document
    # terms in query should only be separated by blank spaces
    def relevance(self, doc_id, query):
        score = 0
        terms = query.split()

        doc_length = self.get_doc_length(doc_id)
        avg_doc_length = self.get_average_doc_length()

        for term in terms:
            term_freq = self.get_term_frequency_in_doc(term, doc_id)
            counter = term_freq * (self.k + 1)
            denominator = term_freq + self.k * (1 - self.b + self.b * doc_length/avg_doc_length)
            idf = self.idf_weight_2(term)
            # relevance score of term in current document
            term_score = idf * counter/denominator
            score = score + term_score
        return score

    # query: input as string separated by whitespaces
    # computes relevance score for each document
    def compute_relevance_on_corpus(self, query):
        scores = {}
        for doc_id, terms in self.documents.items():
            score = self.relevance(doc_id, query)
            scores.update({doc_id: score})
        return scores
