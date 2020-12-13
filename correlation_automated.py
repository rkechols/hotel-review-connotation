from scipy.stats import pearsonr as pearson_r
from typing import List, Tuple
from util import get_correlation_file_name, get_search_results_file_name, LEMMA_GROUPS_LIST, UTF_8


RATING_LEVELS = [1, 2, 3, 4, 5]


def calculate_correlation(scores: List[float]) -> Tuple[float, float, float]:
	r, p = pearson_r(RATING_LEVELS, scores)
	return r, pow(r, 2), p


if __name__ == "__main__":
	for group in LEMMA_GROUPS_LIST:
		search_results_file_name = get_search_results_file_name(group)
		with open(search_results_file_name, "r", encoding=UTF_8) as scores_file:
			correlation_file_name = get_correlation_file_name(group)
			with open(correlation_file_name, "w", encoding=UTF_8) as correlation_file:
				print("lemma,r,r-squared,p-value", file=correlation_file)
				for i, line_ in enumerate(scores_file):
					if i == 0:
						continue  # skip the header
					line_split = line_.strip().split(",")
					lemma = line_split[0]
					scores_str = line_split[1:]
					r_value, r_squared, p_value = calculate_correlation([float(x) for x in scores_str])
					print(f"{lemma},{r_value},{r_squared},{p_value}", file=correlation_file)
	print("completed calculating correlations of TF-IDF scores with rating level")
