from collections import defaultdict
from functools import reduce
from typing import Union, List, Tuple, Iterable

from nltk import word_tokenize

from utils import timer, load_wapo, cleanhtml, CLEANR
from text_processing import TextProcessing
from customized_text_processing import CustomizedTextProcessing
from mongo_db import insert_db_index, query_db_index

text_processor = TextProcessing.from_nltk()

custom = CustomizedTextProcessing.from_customized()
# include your customized text processing class


@timer
def build_inverted_index(wapo_docs: Iterable) -> None:
    """
    load wapo_pa3.jl to build the inverted index and insert the index by using mongo_db.insert_db_index method
    :param wapo_docs:
    :return:
    """
    # TODO:
    index_list = []
    prev_tokens = set()
    tok_doc_dict = defaultdict()

    # get all tokens mapped to their respective postings list

    for doc in wapo_docs:
        normalized_doc = text_processor.get_normalized_tokens(doc['title'], doc['content_str'])
        for token in normalized_doc:
            if token not in prev_tokens:
                tok_doc_dict[token] = [doc['id']]
                prev_tokens.add(token)
            else:
                tok_doc_dict[token].append(doc['id'])

    # convert dict of tokens and posting lists to correct format
    for tok, doc in tok_doc_dict.items():
        set_doc = set(doc)
        index_list.append({'token': tok, 'doc_ids': sorted(list(set_doc))})

    insert_db_index(sorted(index_list, key=lambda i: len(i['doc_ids'])))


def intersection(posting_lists: List[List[int]]) -> List[int]:
    """
    implementation of the intersection of a list of posting lists that have been ordered from the shortest to the longest
    :param posting_lists:
    :return:
    """
    # TODO:
    # use set intersection starting from shortest postings list
    intersect = posting_lists[0]

    for i in range(len(posting_lists)-1):
        if len(posting_lists[i+1]) > 0:
            intersect = list(set(intersect) & set(posting_lists[i+1]))

    return intersect


def query_inverted_index(query: str) -> Tuple[List[int], List[str], List[str]]:
    """
    conjunctive query over the built index by using mongo_db.query_db_index method
    return a list of matched document ids, a list of stop words and a list of unknown words separately
    :param query: user input query
    :return:
    """
    # TODO:
    matched_doc_ids = []
    sw_in_query = []
    unknown_words = []
    # check if word is a stopword
    for token in word_tokenize(query):
        if token in text_processor.STOP_WORDS:
            sw_in_query.append(token)
    # normalize query
    for token in text_processor.get_normalized_tokens('', query):
        result = query_db_index(token)
        if result:
            post_dict = query_db_index(token)
            post_list = post_dict['doc_ids']
            matched_doc_ids.append(post_list)

        else:   # if token can't be queried
            unknown_words.append(token)
    if matched_doc_ids:
        # intersect postings lists
        intersected_ids = intersection(matched_doc_ids)

        # if postings exist but too specific of a search
        if len(intersected_ids) == 0:
            intersected_ids = [-1]
    else:
        intersected_ids = [-1]
    return intersected_ids, sw_in_query, unknown_words
