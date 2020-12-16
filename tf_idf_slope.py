import numpy as np
from typing import Dict, List
from util import AUTOMATED_DIR, get_tf_idf_file_name, SLOPES_FILE_NAME, UTF_8


RATING_LEVELS = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
X_SQUARED_SUM = (RATING_LEVELS * RATING_LEVELS).sum()
SUM_X = RATING_LEVELS.sum()
SQUARE_OF_SUM_X = pow(SUM_X, 2)
N = RATING_LEVELS.shape[0]

DISTRIBUTION_FILE_NAME = AUTOMATED_DIR + "tfidf_distributions.csv"


def get_score_distributions() -> Dict[str, List[float]]:
	to_return = dict()
	for i in range(N):
		rating_level = i + 1
		tf_idf_file_name = get_tf_idf_file_name(rating_level)
		with open(tf_idf_file_name, "r", encoding=UTF_8) as scores_file:
			for line_num, line in enumerate(scores_file):
				if line_num == 0:
					continue  # skip the header
				line_split = line.strip().split(",")
				lemma = line_split[0]
				score = float(line_split[1])
				if lemma not in to_return:
					to_return[lemma] = [0.0] * N
				to_return[lemma][i] = score
	return to_return


def calculate_least_squares_slope(y: np.ndarray) -> float:
	sum_y = y.sum()
	x_y = RATING_LEVELS * y
	numerator = (N * x_y.sum()) - (SUM_X * sum_y)
	denominator = (N * X_SQUARED_SUM) - SQUARE_OF_SUM_X
	return numerator / denominator


if __name__ == "__main__":
	all_tf_idf_distributions = get_score_distributions()
	with open(DISTRIBUTION_FILE_NAME, "w", encoding=UTF_8) as distributions_file:
		print(",".join(["lemma"] + [str(x + 1) for x in range(N)]), file=distributions_file)
		with open(SLOPES_FILE_NAME, "w", encoding=UTF_8) as slopes_file:
			print("lemma,slope", file=slopes_file)
			for lemma_, distribution in all_tf_idf_distributions.items():
				print(",".join([lemma_] + ["{:.8f}".format(tf_idf) for tf_idf in distribution]), file=distributions_file)
				slope = calculate_least_squares_slope(np.array(distribution))
				print(f"{lemma_},{slope}", file=slopes_file)
	print("completed calculating estimated slopes of least-squares solutions of TF-IDF scores with rating level")
