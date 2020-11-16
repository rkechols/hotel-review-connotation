import sys
import multiprocessing as mp
import os
from tokenize_english import read_tks_file
from util import count_lemma_in_tokens, get_tokenized_file_name, tokens_to_str, UTF_8


CONTEXTS_DIR = "./data/contexts/"
CONTEXT_FILE_NAME_F = CONTEXTS_DIR + "{}/{}_context_{}.txt"


def get_context_file_name(lemma: str, rating_level: int) -> str:
	return CONTEXT_FILE_NAME_F.format(lemma, lemma, rating_level)


def find_in_context_all(lemma: str) -> str:
	lemma_dir = CONTEXTS_DIR + lemma
	if not os.path.isdir(lemma_dir):
		os.mkdir(lemma_dir)
	for i in range(5):
		rating_level = i + 1
		doc = read_tks_file(get_tokenized_file_name(rating_level))
		with open(get_context_file_name(lemma, rating_level), "w", encoding=UTF_8) as context_file:
			for line_num, tokenized_review in enumerate(doc, start=1):
				if count_lemma_in_tokens(lemma, tokenized_review) != 0:
					print(f"{line_num}:\t{tokens_to_str(tokenized_review)}", file=context_file)
	return lemma


if __name__ == "__main__":
	if not os.path.exists(CONTEXTS_DIR):
		os.mkdir(CONTEXTS_DIR)
	words = sys.argv[1:]
	with mp.Pool() as pool:
		for word in pool.imap_unordered(find_in_context_all, words):
			print(f"search for \"{word}\" complete")
