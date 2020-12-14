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

SCORES_DIR = "./data/scores/"
SCORES_FILE_NAME_F = SCORES_DIR + "{}-star_scores.csv"

GROUPS_DIR = "./data/lemma_groups/"
LEMMA_GROUP_FILE_NAME_F = GROUPS_DIR + "{}_lemmas.txt"

SEARCH_RESULTS_GROUP_DIR = "./data/scores/{}/"
SEARCH_RESULTS_CSV_F = "{}_search_results.csv"
CORRELATIONS_CSV_F = "{}_correlations.csv"

MANUAL_SCORES_DIR = "./data/manual/"
MANUAL_SCORES_CSV_F = MANUAL_SCORES_DIR + "manual_scores_{}.csv"


def get_rating_level_file_name(rating_level: int) -> str:
	return TXT_FILE_NAME_F.format(rating_level)


def get_tokenized_file_name(rating_level: int) -> str:
	return TOKENIZED_FILE_NAME_F.format(rating_level)


def get_scores_file_name(rating_level: int) -> str:
	return SCORES_FILE_NAME_F.format(rating_level)


def count_lemma_in_tokens(lemma: str, tokens: List[SimpleToken]) -> int:
	count = 0
	for t in tokens:
		if t.lemma == lemma:
			count += 1
	return count


def tokens_to_str(tokens: List[SimpleToken]) -> str:
	return " ".join((t.text for t in tokens))


def get_lemma_group_file_name(group_name: str) -> str:
	return LEMMA_GROUP_FILE_NAME_F.format(group_name)


def read_lemmas_file(group_name: str) -> List[str]:
	to_return = list()
	with open(get_lemma_group_file_name(group_name), "r", encoding=UTF_8) as lemma_file:
		for line in lemma_file:
			lemma = line.strip()
			if lemma != "":
				to_return.append(lemma)
	return to_return


def get_scores_group_dir_name(group_name: str) -> str:
	return SEARCH_RESULTS_GROUP_DIR.format(group_name)


def get_search_results_file_name(group_name: str) -> str:
	return get_scores_group_dir_name(group_name) + SEARCH_RESULTS_CSV_F.format(group_name)


def get_correlation_file_name(group_name: str) -> str:
	return get_scores_group_dir_name(group_name) + CORRELATIONS_CSV_F.format(group_name)


def get_manual_scores_file_name(group_name: str) -> str:
	return MANUAL_SCORES_CSV_F.format(group_name)
