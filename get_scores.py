import os
import re
from typing import Dict
from util import get_scores_file_name, get_search_results_file_name, get_scores_group_dir_name, LEMMA_GROUPS_LIST, read_lemmas_file, UTF_8


SCORES_LINE_RE = re.compile(r"\"(.*)\",(.*),(.*),(.*)")


class Score:
	def __init__(self, tf_idf: float, count_in_doc: int, present_in_doc_count: int):
		self.tf_idf = tf_idf
		self.count_in_doc = count_in_doc
		self.present_in_doc_count = present_in_doc_count


def load_scores(rating_level: int) -> Dict[str, Score]:
	to_return = dict()
	scores_file_name = get_scores_file_name(rating_level)
	with open(scores_file_name, "r", encoding=UTF_8) as scores_file:
		first_line = True
		for line in scores_file:
			if first_line:
				first_line = False
				continue
			match = SCORES_LINE_RE.fullmatch(line.strip())
			lemma = match.group(1)
			tf_idf = float(match.group(2))
			count = int(match.group(3))
			present = int(match.group(4))
			to_return[lemma] = Score(tf_idf, count, present)
	return to_return


def find_score(lemma: str, scores: Dict[str, Score]) -> Score:
	if lemma in scores:
		return scores[lemma]
	else:
		return Score(0, 0, -1)


if __name__ == "__main__":
	for group in LEMMA_GROUPS_LIST:
		group_dir_name = get_scores_group_dir_name(group)
		if not os.path.exists(group_dir_name):
			os.mkdir(group_dir_name)
		search_results_csv = get_search_results_file_name(group)
		lemmas_in_group = read_lemmas_file(group)
		word_to_scores = dict()
		for i_ in range(5):
			level = i_ + 1
			level_scores = load_scores(level)
			for word in lemmas_in_group:
				if word not in word_to_scores:
					word_to_scores[word] = list()
				word_to_scores[word].append(find_score(word, level_scores))
		with open(search_results_csv, "w", encoding=UTF_8) as out_file:
			print("lemma,1-star,2-star,3-star,4-star,5-star", file=out_file)
			for word, score_list in word_to_scores.items():
				word_q = "\"" + word + "\""
				print(",".join([word_q] + ["{:.8f}".format(s.tf_idf) for s in score_list]), file=out_file)
		print(f"results printed to {search_results_csv}")
