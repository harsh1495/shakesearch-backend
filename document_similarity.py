import os
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from global_variables import EMBEDDINGS_DICTIONARY, TF_IDF_MATRIX, SIMILARITY_MATRIX, FINAL_FILE_NAMES


class DocumentSimilarity:
    def __init__(self, processed_query):
        self.processed_query = processed_query

    def generate_unigrams_bigrams(self):
        '''
        Generate unigrams and bigrams from the query
        '''
        query_doc = []
        tokens = word_tokenize(self.processed_query)
        query_doc.extend(tokens)
        bigrm = nltk.bigrams(tokens)
        for bg in bigrm:
            query_doc.append(' '.join(bg))

        return query_doc

    def find_similar_documents(self):
        '''
        Find all documents that match with the query
        '''
        query_doc = self.generate_unigrams_bigrams()
        query_doc_bow = EMBEDDINGS_DICTIONARY.doc2bow(query_doc)

        # perform a similarity query against the corpus
        query_doc_tf_idf = TF_IDF_MATRIX[query_doc_bow]
        results = SIMILARITY_MATRIX[query_doc_tf_idf]
        return results

    def check_threshold(self, current_score, max_score):
        '''
        Check whether the current score meets the threshold for it to be a valid result
        Threshold logic - Should be greater than 10% of the highest score
        TODO: Strengthen threshold logic
        '''
        if max_score <= 0.1:
            if current_score >= 0.05:
                return True
            else:
                return False

        if current_score > 0.1 * max_score:
            return True
        else:
            return False

    def filter_top_pages(self, results):
        '''
        Sort and filter the results and return a list of tuple containing the name of the file (page), name of the book and the similarity score
        '''
        max_score = sorted(results, reverse=True)[0]
        top_results_idx = results.argsort()[::-1]

        top_pages = []
        for idx in top_results_idx:
            if results[idx] != 0 and self.check_threshold(results[idx], max_score):
                filename = FINAL_FILE_NAMES[idx]
                document_name = filename[:filename.find("_page")].upper()
                top_pages.append((filename, document_name, results[idx]))

        return top_pages

    def generate_search_results(self):
        '''
        Run methods to compute the similarity of the query to the corpus of documents and return the top search results that meet a threshold
        '''
        search_results = self.find_similar_documents()
        top_search_results = self.filter_top_pages(search_results)

        return top_search_results
