import os
from typing import List
from simple_token import SimpleToken


UTF_8 = "utf8"
SPACY_ENGLISH_NAME = "en"
DICTIONARY_FILE_NAME = "./data/reviews_dictionary.gendict"
LEMMA_GROUPS_LIST = ["random", "noun", "adjective"]

SPLIT_DIR = "./data/split/"
TXT_FILE_NAME_F = SPLIT_DIR + "tripadvisor_{}-star.txt"

TOKENIZED_DIR = "./data/tokenized/"
TOKENIZED_FILE_NAME_F = TOKENIZED_DIR + "{}-star-tokenized.tks"

AUTOMATED_DIR = "./data/automated/"
TF_IDF_DIR = AUTOMATED_DIR + "tf-idf/"
TF_IDF_FILE_NAME_F = TF_IDF_DIR + "{}-star.csv"
SLOPES_FILE_NAME = AUTOMATED_DIR + "slopes.csv"
SCORES_FILE_NAME = AUTOMATED_DIR + "all_scores.csv"
SEARCH_DIR = AUTOMATED_DIR + "search/"
SEARCH_RESULTS_CSV_F = SEARCH_DIR + "{}_search_results.csv"

GROUPS_DIR = "./data/lemma_groups/"
LEMMA_GROUP_FILE_NAME_F = GROUPS_DIR + "{}_lemmas.txt"

MANUAL_SCORES_DIR = "./data/manual/"
MANUAL_SCORES_CSV_F = MANUAL_SCORES_DIR + "manual_scores_{}.csv"


def ensure_dir(dir_name: str):
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)


def get_rating_level_file_name(rating_level: int) -> str:
	ensure_dir(SPLIT_DIR)
	return TXT_FILE_NAME_F.format(rating_level)


def get_tokenized_file_name(rating_level: int) -> str:
	ensure_dir(TOKENIZED_DIR)
	return TOKENIZED_FILE_NAME_F.format(rating_level)


def get_tf_idf_file_name(rating_level: int) -> str:
	ensure_dir(AUTOMATED_DIR)
	ensure_dir(TF_IDF_DIR)
	return TF_IDF_FILE_NAME_F.format(rating_level)


def count_lemma_in_tokens(lemma: str, tokens: List[SimpleToken]) -> int:
	count = 0
	for t in tokens:
		if t.lemma == lemma:
			count += 1
	return count


def tokens_to_str(tokens: List[SimpleToken]) -> str:
	return " ".join((t.text for t in tokens))


def get_lemma_group_file_name(group_name: str) -> str:
	ensure_dir(GROUPS_DIR)
	return LEMMA_GROUP_FILE_NAME_F.format(group_name)


def read_lemmas_file(group_name: str) -> List[str]:
	to_return = list()
	with open(get_lemma_group_file_name(group_name), "r", encoding=UTF_8) as lemma_file:
		for line in lemma_file:
			lemma = line.strip()
			if lemma != "":
				to_return.append(lemma)
	return to_return


def get_search_results_file_name(group_name: str) -> str:
	ensure_dir(AUTOMATED_DIR)
	ensure_dir(SEARCH_DIR)
	return SEARCH_RESULTS_CSV_F.format(group_name)


def get_manual_scores_file_name(group_name: str) -> str:
	ensure_dir(MANUAL_SCORES_DIR)
	return MANUAL_SCORES_CSV_F.format(group_name)
