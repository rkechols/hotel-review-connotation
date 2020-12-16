import numpy as np
from typing import List, Tuple
from util import SCORES_FILE_NAME, SLOPES_FILE_NAME, UTF_8


def read_slopes_file() -> Tuple[List[str], List[float]]:
	lemmas = list()
	slopes = list()
	with open(SLOPES_FILE_NAME, "r", encoding=UTF_8) as slopes_file:
		for i, line in enumerate(slopes_file):
			if i == 0:  # skip the header
				continue
			line_split = line.strip().split(",")
			lemmas.append(line_split[0])
			slopes.append(float(line_split[1]))
	return lemmas, slopes


def calculate_adjusted_scores(scores: List[float], stddev: float) -> List[float]:
	scores = np.array(scores)
	scores = scores / stddev
	scores = np.tanh(scores)
	return [scores[i] for i in range(scores.shape[0])]


if __name__ == "__main__":
	# calculate standard deviation of all slopes
	all_lemmas, all_slopes = read_slopes_file()
	standard_deviation = np.array(all_slopes).std()
	# calculate adjusted scores
	adjusted_scores = calculate_adjusted_scores(all_slopes, standard_deviation)
	with open(SCORES_FILE_NAME, "w", encoding=UTF_8) as out_file:
		print("lemma,adjusted automated score", file=out_file)
		for lemma, score in zip(all_lemmas, adjusted_scores):
			print(f"{lemma},{score}", file=out_file)
	print(f"all automated scores printed to {SCORES_FILE_NAME}")
