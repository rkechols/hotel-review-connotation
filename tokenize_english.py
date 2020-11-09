import spacy
from typing import Dict, List
from spacy.tokens import Doc, Token
from util import get_rating_level_file_name, SPACY_ENGLISH_NAME, UTF_8
import multiprocessing as mp


def tokenize_file(rating_level: int) -> List[List[Token]]:
	file_name = get_rating_level_file_name(rating_level)
	spacy_en = spacy.load(SPACY_ENGLISH_NAME)
	to_return = list()
	with open(file_name, "r", encoding=UTF_8) as txt_file:
		for line_num, review_text in enumerate(txt_file, start=1):
			review_tokens: Doc = spacy_en(review_text)
			to_return.append(list(review_tokens))
			break
	return to_return


def get_all_tokenized_ratings() -> Dict[int, List[List[Token]]]:
	to_return = dict()
	with mp.Pool() as pool:
		tokenized_file_generator = pool.imap(tokenize_file, range(1, 6))
		for rating_level, tokenized_file in enumerate(tokenized_file_generator, start=1):
			to_return[rating_level] = tokenized_file
	return to_return
