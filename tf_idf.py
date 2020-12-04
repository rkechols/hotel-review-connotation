import math
import os
from typing import Dict, List, Set, Tuple
# from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from tokenize_english import read_tks_file_flat
from util import get_scores_file_name, get_tokenized_file_name, SCORES_DIR, UTF_8


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
	if os.path.exists(DICTIONARY_FILE_NAME):
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


def get_bags_of_word_ids(corpus: Dict[int, Bow]) -> Dict[int, Set[int]]:
	to_return = dict()
	for rating_level, bow in corpus.items():
		this_set = set()
		for word_id, _ in bow:
			this_set.add(word_id)
		to_return[rating_level] = this_set
	return to_return


class ScoreInfo:
	def __init__(self, word_id: int, tf_idf: float, count_in_doc: int, present_in_doc_count: int):
		self.word_id = word_id
		self.tf_idf = tf_idf
		self.count_in_doc = count_in_doc
		self.present_in_doc_count = present_in_doc_count

	def __lt__(self, other):
		if not isinstance(other, ScoreInfo):
			raise ValueError(f"cannot be compared with non-{self.__class__.__name__} object; received object of class {other.__class__.__name__}")
		return self.tf_idf < other.tf_idf


def get_tf_idf_scores(corpus: Dict[int, Bow], token_counts: Dict[int, int], bags_of_ids: Dict[int, Set[int]]) -> Dict[int, List[ScoreInfo]]:
	doc_count = len(bags_of_ids)
	to_return = dict()
	for rating_level, bow in corpus.items():
		doc_size = token_counts[rating_level]
		these_scores = list()
		for word_id, count in bow:
			tf = count / doc_size
			present_in_doc_count = 0
			for bag_of_ids in bags_of_ids.values():
				if word_id in bag_of_ids:
					present_in_doc_count += 1
			idf = 1 + math.log(doc_count / (1 + present_in_doc_count))
			these_scores.append(ScoreInfo(word_id, tf * idf, count, present_in_doc_count))
		these_scores.sort(reverse=True)  # sort by score, big to small
		to_return[rating_level] = these_scores
	return to_return


def save_scores_to_files(dictionary: Dictionary, scores: Dict[int, List[ScoreInfo]]):
	scores_dir = SCORES_DIR
	print(f"saving scores to files in {scores_dir}")
	if not os.path.isdir(scores_dir):
		os.mkdir(scores_dir)
	for rating_level, scores_list in scores.items():
		with open(get_scores_file_name(rating_level), "w", encoding=UTF_8) as scores_file:
			# print the header
			print("lemma,score,count in doc,in how many docs", file=scores_file)
			for s in scores_list:
				print(f"\"{dictionary[s.word_id]}\",{s.tf_idf},{s.count_in_doc},{s.present_in_doc_count}", file=scores_file)


if __name__ == "__main__":
	docs = get_lemmatized_documents()
	t_counts = get_document_token_counts(docs)
	print("----------")
	print(f"total token count: {sum(t_counts.values())}")
	print("----------")
	d = get_dictionary(docs)
	corp = get_corpus(docs, d)
	print("----------")
	print(f"total type count: {len(d)}")
	print("----------")
	for r_level, bag in corp.items():
		print(f"types in all {r_level}-star reviews: {len(bag)}")
	print("----------")
	print("calculating tf-idf scores...")
	bags_of_just_ids = get_bags_of_word_ids(corp)
	all_scores = get_tf_idf_scores(corp, t_counts, bags_of_just_ids)
	save_scores_to_files(d, all_scores)
	print("done!")
