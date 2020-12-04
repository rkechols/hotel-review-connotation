from typing import List
from simple_token import SimpleToken


UTF_8 = "utf8"
SPACY_ENGLISH_NAME = "en"

SPLIT_DIR = "./data/split/"
TXT_FILE_NAME_F = SPLIT_DIR + "tripadvisor_{}-star.txt"

TOKENIZED_DIR = "./data/tokenized/"
TOKENIZED_FILE_NAME_F = TOKENIZED_DIR + "{}-star-tokenized.tks"

SCORES_DIR = "./data/scores/"
SCORES_FILE_NAME_F = SCORES_DIR + "{}-star_scores.csv"


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
