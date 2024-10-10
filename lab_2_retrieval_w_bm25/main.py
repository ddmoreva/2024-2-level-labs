"""
Lab 2.

Text retrieval with BM25
"""
# pylint:disable=too-many-arguments, unused-argument
import re
import math


def tokenize(text: str) -> list[str] | None:
    """
    Tokenize the input text into lowercase words without punctuation, digits and other symbols.

    Args:
        text (str): The input text to tokenize.

    Returns:
        list[str] | None: A list of words from the text.

    In case of corrupt input arguments, None is returned.
    """
    if not isinstance(text, str):
        return None
    lower = text.lower()
    list_for_words = re.findall('[a-zа-я]+', lower)
    return list_for_words


def remove_stopwords(tokens: list[str], stopwords: list[str]) -> list[str] | None:
    """
    Remove stopwords from the list of tokens.

    Args:
        tokens (list[str]): List of tokens.
        stopwords (list[str]): List of stopwords.

    Returns:
        list[str] | None: Tokens after removing stopwords.

    In case of corrupt input arguments, None is returned.
    """
    if tokens is None or stopwords is None:
        return None
    if (not isinstance(tokens, list) or not isinstance(stopwords, list) or
            not all(isinstance(i, str) for i in tokens) or
            not all(isinstance(k, str) for k in stopwords)):
        return None
    if not tokens or not stopwords:
        return None
    without_stop = []
    for word in tokens:
        if word not in stopwords:
            without_stop.append(word)
    return without_stop


def build_vocabulary(documents: list[list[str]]) -> list[str] | None:
    """
    Build a vocabulary from the documents.

    Args:
        documents (list[list[str]]): List of tokenized documents.

    Returns:
        list[str] | None: List with unique words from the documents.

    In case of corrupt input arguments, None is returned.
    """
    if not documents:
        return None
    if not isinstance(documents, list):
        return None
    if not all(isinstance(item, list) and all(isinstance(elem, str)
                                              for elem in item) for item in documents):
        return None
    main_list = []
    for words in documents:
        for word in words:
            if word not in main_list:
                main_list.append(word)
    return main_list


def calculate_tf(vocab: list[str], document_tokens: list[str]) -> dict[str, float] | None:
    """
    Calculate term frequency for the given tokens based on the vocabulary.

    Args:
        vocab (list[str]): Vocabulary list.
        document_tokens (list[str]): Tokenized document.

    Returns:
        dict[str, float] | None: Mapping from vocabulary terms to their term frequency.

    In case of corrupt input arguments, None is returned.
    """
    if not vocab or not document_tokens:
        return None
    if vocab is None or document_tokens is None:
        return None
    if (not isinstance(vocab, list) or not isinstance(document_tokens, list) or
            not all(isinstance(i, str) for i in document_tokens) or
            not all(isinstance(k, str) for k in vocab)):
        return None
    dictionary_for_tf = {}
    for word in vocab:
        dictionary_for_tf[word] = 0.0
        if word in document_tokens:
            dictionary_for_tf[word] = document_tokens.count(word) / len(document_tokens)
    for signal in document_tokens:
        if signal in dictionary_for_tf:
            continue
        else:
            dictionary_for_tf[signal] = document_tokens.count(signal) / len(document_tokens)
    return dictionary_for_tf

print(calculate_tf(['school', 'tower', 'go', 'used', 'magic', 'perfect', 'cat', 'dogs',
                    'best', 'top', 'studying', 'pets', 'leave', 'parrots', 'morning', 'hill',
                    'loved', 'picnic', 'rarely', 'boy', 'every', 'weather', 'steven', 'two', 'three',
                    'spells', 'wizard', 'home', 'leaved', 'date', 'friend', 'dragon', 'sad', 'princess',
                    'wand', 'summer'], ['dragon', 'princess', 'picnic', 'date', 'top',
                                        'hill', 'rarely', 'leaved', 'tower', 'summer', 'weather', 'perfect',
                                        'hill', 'picnic']))

def calculate_idf(vocab: list[str], documents: list[list[str]]) -> dict[str, float] | None:
    """
    Calculate inverse document frequency for each term in the vocabulary.

    Args:
        vocab (list[str]): Vocabulary list.
        documents (list[list[str]]): List of tokenized documents.

    Returns:
        dict[str, float] | None: Mapping from vocabulary terms to its IDF scores.

    In case of corrupt input arguments, None is returned.
    """
    if not vocab or not documents:
        return None
    if (not isinstance(vocab, list) or not isinstance(documents, list) or
            not all(isinstance(p, str) for p in vocab) or
            not all(isinstance(k, list) and all(isinstance(elem, str)
                                                for elem in k) for k in documents)):
        return None
    counter_for_documents = len(documents)
    dictionary_for_idf = {}
    for word in vocab:
        dictionary_for_idf[word] = 0.0
        counter = 0.0
        for freq in documents:
            if word in freq:
                counter += 1.0
            value = (counter_for_documents - counter + 0.5)/(counter + 0.5)
            dictionary_for_idf[word] = math.log(value)
    return dictionary_for_idf

print(calculate_idf(['school', 'tower', 'go', 'used', 'magic', 'perfect', 'cat',
                     'dogs', 'best', 'top', 'studying', 'pets', 'leave', 'parrots', 'morning',
                     'hill', 'loved', 'picnic', 'rarely', 'boy', 'every', 'weather', 'steven', 'two',
                     'three', 'spells', 'wizard', 'home', 'leaved', 'date', 'friend', 'dragon', 'sad',
                     'princess', 'wand', 'summer'], [['boy', 'wizard', 'used', 'wand', 'spells',
                                                      'studying', 'magic', 'school', 'best', 'friend', 'wizard'],
                                                     ['steven', 'boy', 'loved', 'pets', 'cat', 'two', 'dogs', 'three',
                                                      'parrots', 'every', 'morning', 'want', 'go', 'school', 'leave',
                                                      'pets', 'home'], ['dragon', 'princess', 'picnic', 'date', 'top',
                                                                        'hill', 'rarely', 'leaved', 'tower', 'summer',
                                                                        'weather', 'perfect', 'hill', 'picnic']]))


def calculate_tf_idf(tf: dict[str, float], idf: dict[str, float]) -> dict[str, float] | None:
    """
    Calculate TF-IDF scores for a document.

    Args:
        tf (dict[str, float]): Term frequencies for the document.
        idf (dict[str, float]): Inverse document frequencies.

    Returns:
        dict[str, float] | None: Mapping from terms to their TF-IDF scores.

    In case of corrupt input arguments, None is returned.
    """
    if not tf or not idf:
        return None
    if not isinstance(tf, dict) or not isinstance(idf, dict):
        return None
    if (not all(isinstance(key, str) for key in tf.keys()) or
            not all(isinstance(value, float) for value in tf.values())):
        return None
    if (not all(isinstance(key, str) for key in idf.keys()) or
            not all(isinstance(value, float) for value in idf.values())):
        return None
    dictionary_for_result = {}
    for key, value in tf.items():
        dictionary_for_result[key] = 0.0
        if key in idf.keys():
            dictionary_for_result[key] = (tf[key] * idf[key])
    return dictionary_for_result

print(calculate_tf_idf({'school': 0.0, 'tower': 0.071, 'go': 0.0, 'used': 0.0, 'magic': 0.0,
                        'perfect': 0.071, 'cat': 0.0, 'dogs': 0.0, 'best': 0.0, 'top': 0.071,
                        'studying': 0.0, 'pets': 0.0, 'leave': 0.0, 'parrots': 0.0, 'morning': 0.0,
                        'hill': 0.143, 'loved': 0.0, 'picnic': 0.143, 'rarely': 0.071, 'boy': 0.0,
                        'every': 0.0, 'weather': 0.071, 'steven': 0.0, 'two': 0.0, 'three': 0.0,
                        'spells': 0.0, 'wizard': 0.0, 'home': 0.0, 'leaved': 0.071, 'date': 0.071,
                        'friend': 0.0, 'dragon': 0.071, 'sad': 0.0, 'princess': 0.071, 'wand': 0.0,
                        'summer': 0.071}, {'school': -0.51, 'tower': 0.51, 'go': 0.51,
                                           'used': 0.51, 'magic': 0.51, 'perfect': 0.51, 'cat': 0.51,
                                           'dogs': 0.51, 'best': 0.51, 'top': 0.51, 'studying': 0.51,
                                           'pets': 0.51, 'leave': 0.51, 'parrots': 0.51, 'morning': 0.51,
                                           'hill': 0.51, 'loved': 0.51, 'picnic': 0.51, 'rarely': 0.51,
                                           'boy': -0.51, 'every': 0.51, 'weather': 0.51, 'steven': 0.51,
                                           'two': 0.51, 'three': 0.51, 'spells': 0.51, 'wizard': 0.51,
                                           'home': 0.51, 'leaved': 0.51, 'date': 0.51, 'friend': 0.51,
                                           'dragon': 0.51, 'sad': 1.95, 'princess': 0.51,
                                           'wand': 0.51, 'summer': 0.51}))

def calculate_bm25(
    vocab: list[str],
    document: list[str],
    idf_document: dict[str, float],
    k1: float = 1.5,
    b: float = 0.75,
    avg_doc_len: float | None = None,
    doc_len: int | None = None,
) -> dict[str, float] | None:
    """
    Calculate BM25 scores for a document.

    Args:
        vocab (list[str]): Vocabulary list.
        document (list[str]): Tokenized document.
        idf_document (dict[str, float]): Inverse document frequencies.
        k1 (float): BM25 parameter.
        b (float): BM25 parameter.
        avg_doc_len (float | None): Average document length.
        doc_len (int | None): Length of the document.

    Returns:
        dict[str, float] | None: Mapping from terms to their BM25 scores.

    In case of corrupt input arguments, None is returned.
    """
    if not isinstance(vocab, list) or not all(isinstance(value, str) for value in vocab):
        return None
    if not isinstance(document, list) or not all(isinstance(value, str) for value in document):
        return None
    if (not isinstance(idf_document, dict) or not all(isinstance(key, str) for key in idf_document) or
            not all(isinstance(value, float) for value in idf_document)):
        return None
    if not 1.2 <= k1 <= 2.0 or not 0 <= b <= 1:
        return None
    if (avg_doc_len is None or avg_doc_len <= 0 or
            doc_len is None or doc_len <= 0):
        return None
    bm25 = {}
    set_for_idf = set(i for i in idf_document.keys()) #я его создала, чтобы сравнить с vocab - чтобы все слова были в нем
    set_for_vocab = set(vocab)
    if set_for_vocab.difference(set_for_idf) == 0:
        for key, value in idf_document.items():
            if key in vocab:
                bm25[key] = ((value * (document.count(key) * (k1 + 1))) /
                             (document.count(key) + k1 * (1 - b + ((b * doc_len) / avg_doc_len))))
    else:
        return None
    return bm25


def rank_documents(
    indexes: list[dict[str, float]], query: str, stopwords: list[str]
) -> list[tuple[int, float]] | None:
    """
    Rank documents for the given query.

    Args:
        indexes (list[dict[str, float]]): List of BM25 or TF-IDF indexes for the documents.
        query (str): The query string.
        stopwords (list[str]): List of stopwords.

    Returns:
        list[tuple[int, float]] | None: Tuples of document index and its score in the ranking.

    In case of corrupt input arguments, None is returned.
    """
    if (not isinstance(query, str) or not isinstance(stopwords, list) or
            not all(isinstance(i, str) for i in stopwords) or not isinstance(indexes, list)
            or not all(isinstance(k, dict) for k in indexes)):
        return None
    for index in indexes:
        if not isinstance(index, dict):
            return None
        for key, value in index.items():
            if not isinstance(key, str) or not isinstance(value, float):
                return None
    letters = tokenize(query)
    without_stopwords = remove_stopwords(letters, stopwords) #реализация прошла успешно, теперь ищем все слова в уже данных
    number_of_documents = len(indexes)
    dict_with_index = {}
    for metrica in indexes:
        value_of_whole_document = 0.0
        for word in without_stopwords:
            if word in metrica.keys():
                value_of_whole_document += metrica[word]
        for index, result in enumerate(dict_with_index.values()):



def calculate_bm25_with_cutoff(
    vocab: list[str],
    document: list[str],
    idf_document: dict[str, float],
    alpha: float,
    k1: float = 1.5,
    b: float = 0.75,
    avg_doc_len: float | None = None,
    doc_len: int | None = None,
) -> dict[str, float] | None:
    """
    Calculate BM25 scores for a document with IDF cutoff.

    Args:
        vocab (list[str]): Vocabulary list.
        document (list[str]): Tokenized document.
        idf_document (dict[str, float]): Inverse document frequencies.
        alpha (float): IDF cutoff threshold.
        k1 (float): BM25 parameter.
        b (float): BM25 parameter.
        avg_doc_len (float | None): Average document length.
        doc_len (int | None): Length of the document.

    Returns:
        dict[str, float] | None: Mapping from terms to their BM25 scores with cutoff applied.

    In case of corrupt input arguments, None is returned.
    """


def save_index(index: list[dict[str, float]], file_path: str) -> None:
    """
    Save the index to a file.

    Args:
        index (list[dict[str, float]]): The index to save.
        file_path (str): The path to the file where the index will be saved.
    """


def load_index(file_path: str) -> list[dict[str, float]] | None:
    """
    Load the index from a file.

    Args:
        file_path (str): The path to the file from which to load the index.

    Returns:
        list[dict[str, float]] | None: The loaded index.

    In case of corrupt input arguments, None is returned.
    """


def calculate_spearman(rank: list[int], golden_rank: list[int]) -> float | None:
    """
    Calculate Spearman's rank correlation coefficient between two rankings.

    Args:
        rank (list[int]): Ranked list of document indices.
        golden_rank (list[int]): Golden ranked list of document indices.

    Returns:
        float | None: Spearman's rank correlation coefficient.

    In case of corrupt input arguments, None is returned.
    """
