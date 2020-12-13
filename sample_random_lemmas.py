import os
import random
from typing import List
from gensim.corpora import Dictionary
from util import DICTIONARY_FILE_NAME, get_lemma_group_file_name, GROUPS_DIR, UTF_8


SAMPLE_SIZE = 50


def get_all_lemmas() -> List[str]:
	gensim_dict = Dictionary.load(DICTIONARY_FILE_NAME)
	assert isinstance(gensim_dict, Dictionary)

	return [k for k in gensim_dict.token2id]


if __name__ == "__main__":
	all_lemmas = get_all_lemmas()
	selected_lemmas = random.sample(all_lemmas, SAMPLE_SIZE)
	if not os.path.exists(GROUPS_DIR):
		os.mkdir(GROUPS_DIR)
	out_file_name = get_lemma_group_file_name("random")
	with open(out_file_name, "w", encoding=UTF_8) as out_file:
		for lemma in selected_lemmas:
			print(lemma, file=out_file)
	print(f"printed {SAMPLE_SIZE} random lemmas to {out_file_name}")
