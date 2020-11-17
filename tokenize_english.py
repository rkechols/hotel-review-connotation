import os
import time
from os import path
import spacy
import re
from typing import Dict, List
from spacy.tokens import Doc, Token
from simple_token import SimpleToken
from util import get_rating_level_file_name, get_tokenized_file_name, SPACY_ENGLISH_NAME, TOKENIZED_DIR, UTF_8
import multiprocessing as mp


token_line_re = re.compile(r"(.*?)\t(.*?)\t(.*)")


def tokenize_file(rating_level: int) -> List[List[SimpleToken]]:
	file_name = get_rating_level_file_name(rating_level)
	spacy_en = spacy.load(SPACY_ENGLISH_NAME)
	to_return = list()
	with open(file_name, "r", encoding=UTF_8) as txt_file:
		for line_num, review_text_ in enumerate(txt_file, start=1):
			review_text = review_text_.strip()
			if review_text == "":
				continue
			review_tokens: Doc = spacy_en(review_text)
			these_tokens = list()
			for t in review_tokens:
				assert isinstance(t, Token)
				these_tokens.append(SimpleToken(t.text, t.lemma_, t.pos_))
			to_return.append(these_tokens)
	return to_return


def get_all_tokenized_ratings() -> Dict[int, List[List[SimpleToken]]]:
	to_return = dict()
	if path.exists(TOKENIZED_DIR):
		print(f"loading tokens from files in {TOKENIZED_DIR}")
		for i in range(5):
			rating_level = i + 1
			doc = read_tks_file(get_tokenized_file_name(rating_level))
			to_return[rating_level] = doc
	else:
		print("running tokenizer...")
		os.mkdir(TOKENIZED_DIR)
		time_tokenize_start = time.time()
		# run the tokenization
		with mp.Pool() as pool:
			tokenized_file_generator = pool.imap(tokenize_file, range(1, 6))
			for rating_level, tokenized_file in enumerate(tokenized_file_generator, start=1):
				to_return[rating_level] = tokenized_file
		# print some info
		time_tokenize_end = time.time()
		print(f"tokenization completed in {time_tokenize_end - time_tokenize_start} seconds")
		write_tokens_to_files(to_return)
	print("----------")
	token_count = 0
	for rating_level, doc in to_return.items():
		this_count = sum(len(rating) for rating in doc)
		print(f"tokens in all {rating_level}-star reviews: {this_count}")
		token_count += this_count
	print("----------")
	print(f"{token_count} tokens total")
	print("----------")
	# return the actual answer
	return to_return


def write_tokens_to_files(docs: Dict[int, List[List[SimpleToken]]]):
	print(f"saving tokenized documents to {TOKENIZED_DIR}")
	for rating_level, ratings in docs.items():
		with open(get_tokenized_file_name(rating_level), "w", encoding=UTF_8) as tokens_file:
			for rating in ratings:
				for token in rating:
					print(f"{token.text}\t{token.lemma}\t{token.part_of_speech}", file=tokens_file)
				print("", file=tokens_file)  # blank line separates ratings


def read_tks_file(tks_file_name: str) -> List[List[SimpleToken]]:
	to_return = list()
	with open(tks_file_name, "r", encoding=UTF_8) as tks_file:
		this_rating = list()
		for line_num, line_ in enumerate(tks_file, start=1):
			# if we see a blank line, that's the division between ratings
			line = line_.strip()
			if line == "":
				if len(this_rating) > 0:
					to_return.append(this_rating)
					this_rating = list()
				continue
			token_match = token_line_re.match(line)
			if token_match is None:
				raise ValueError(f"line {line_num} in file {tks_file_name} did not match the token regex: {line}")
			text, lemma, pos = token_match.group(1), token_match.group(2), token_match.group(3)
			this_rating.append(SimpleToken(text, lemma, pos))
	return to_return


def read_tks_file_flat(tks_file_name: str) -> List[SimpleToken]:
	tokens_by_review = read_tks_file(tks_file_name)
	to_return = list()
	for review in tokens_by_review:
		to_return += review
	return to_return


if __name__ == "__main__":
	get_all_tokenized_ratings()
