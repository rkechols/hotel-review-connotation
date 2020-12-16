from typing import Dict
from util import get_search_results_file_name, LEMMA_GROUPS_LIST, read_lemmas_file, SCORES_FILE_NAME, UTF_8


def load_scores() -> Dict[str, float]:
	to_return = dict()
	with open(SCORES_FILE_NAME, "r", encoding=UTF_8) as scores_file:
		for i, line in enumerate(scores_file):
			if i == 0:  # skip the header
				continue
			line_split = line.strip().split(",")
			lemma = line_split[0]
			score = line_split[1]
			to_return[lemma] = score
	return to_return


if __name__ == "__main__":
	all_scores = load_scores()
	for group in LEMMA_GROUPS_LIST:
		lemmas_in_group = read_lemmas_file(group)
		group_scores = dict()
		for word_ in lemmas_in_group:
			word = '"' + word_ + '"'
			if word in all_scores:
				group_scores[word] = all_scores[word]
			else:
				raise ValueError(f"NO SCORE FOUND FOR LEMMA {word_}")
		search_results_csv = get_search_results_file_name(group)
		with open(search_results_csv, "w", encoding=UTF_8) as out_file:
			print("lemma,automated score", file=out_file)
			for word_, score_ in group_scores.items():
				print(f"{word_},{score_}", file=out_file)
		print(f"results printed to {search_results_csv}")
