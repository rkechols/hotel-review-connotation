from typing import Dict, List, Tuple
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from os import path
from tokenize_english import read_tks_file_flat
from util import get_tokenized_file_name


Bow = List[Tuple[int, int]]

DICTIONARY_FILE_NAME = "./data/reviews_dictionary.gendict"


def get_lemmatized_documents() -> Dict[int, List[str]]:
	print("loading lemmas from tokenized documents...")
	documents = dict()
	for i in range(5):
		rating_level = i + 1
		tks_file_name = get_tokenized_file_name(rating_level)
		tokens = read_tks_file_flat(tks_file_name)
		lemmas = [t.lemma for t in tokens]
		documents[rating_level] = lemmas
	return documents


def get_document_token_counts(documents: Dict[int, List[str]]) -> Dict[int, int]:
	return {rating_level: len(tokens) for rating_level, tokens in documents.items()}


def get_dictionary(documents: Dict[int, List[str]]) -> Dictionary:
	if path.exists(DICTIONARY_FILE_NAME):
		print(f"loading dictionary from {DICTIONARY_FILE_NAME}")
		gensim_dict = Dictionary.load(DICTIONARY_FILE_NAME)
	else:
		print("creating dictionary")
		gensim_dict = Dictionary()
		gensim_dict.add_documents(documents.values())
		print(f"saving dictionary to {DICTIONARY_FILE_NAME}")
		gensim_dict.save(DICTIONARY_FILE_NAME)
	return gensim_dict


def get_corpus(documents: Dict[int, List[str]], dictionary: Dictionary) -> Dict[int, Bow]:
	print("creating corpus (converting documents to BoWs)")
	corpus = dict()
	for rating_level, tokens in documents.items():
		corpus[rating_level] = dictionary.doc2bow(tokens)
	return corpus


if __name__ == "__main__":
	docs = get_lemmatized_documents()
	token_counts = get_document_token_counts(docs)
	print("----------")
	print(f"total token count: {sum(token_counts.values())}")
	print("----------")
	d = get_dictionary(docs)
	corp = get_corpus(docs, d)
	print("----------")
	print(f"total type count: {len(d)}")
	print("----------")
	for r_level, bow in corp.items():
		print(f"types in all {r_level}-star reviews: {len(bow)}")
	print("----------")
