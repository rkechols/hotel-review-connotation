import os
import random
from typing import List
from util import LEMMA_GROUPS_LIST, read_lemmas_file, UTF_8


MANUAL_SCORES_DIR = "./data/manual/"
CONTEXT_FILE_NAME_F = "./data/contexts/{}/{}_context{}.txt"


def get_score(lemma: str, context: str) -> int:
	print(f"CONTEXT: {context}")
	while True:
		response_str = input(f"In this context, is the word '{lemma}' used to say positive (1), neutral (2), or negative (3) things about the hotel?")
		if response_str not in ["1", "2", "3"]:
			print("Invalid response. Enter 1, 2, or 3")
		else:
			response = int(response_str)
			break
	if response == 1:
		return 1
	if response == 2:
		return 0
	else:  # response == 3:
		return -1


def get_average_score(lemma: str, contexts: List[str], sample_size: int = 20) -> float:
	all_scores = list()
	for context in random.sample(contexts, sample_size):
		all_scores.append(get_score(lemma, context))
	return sum(all_scores) / len(all_scores)


def get_context_file_name(lemma: str, rating_level: int) -> str:
	return CONTEXT_FILE_NAME_F.format(lemma, lemma, rating_level)


def read_contexts_files(lemma: str) -> List[str]:
	all_contexts = list()
	for i in range(5):
		rating_level = i + 1
		file_name = get_context_file_name(lemma, rating_level)
		with open(file_name, "r", encoding=UTF_8) as context_file:
			for line_ in context_file:
				line = line_.strip()
				tab_index = line.find("\t")
				if tab_index == -1:
					continue  # error?
				all_contexts.append(line[(tab_index + 1):])  # chop off the line number and tab prefix
	return all_contexts


def manual_scores(list_name: str, lemmas: List[str]):
	with open(MANUAL_SCORES_DIR + f"manual_scores_{list_name}.csv", "w", encoding=UTF_8) as out_file:
		print(f"lemma,manual score", file=out_file)
		for lemma in lemmas:
			context_list = read_contexts_files(lemma)
			score = get_average_score(lemma, context_list)
			print(f"{lemma},{score}", file=out_file)


if __name__ == "__main__":
	if not os.path.exists(MANUAL_SCORES_DIR):
		os.mkdir(MANUAL_SCORES_DIR)
	for group in LEMMA_GROUPS_LIST:
		manual_scores(group, read_lemmas_file(group))
