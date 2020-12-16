from typing import Dict, List, Tuple
from scipy.stats import pearsonr as pearson_r
from util import ensure_dir, get_manual_scores_file_name, get_search_results_file_name, LEMMA_GROUPS_LIST, UTF_8


OUTPUT_DIR = "./data/final/"
OUTPUT_FILE_NAME_F = OUTPUT_DIR + "final_data_points_{}.csv"


def calculate_correlation(x: List[float], y: List[float]) -> Tuple[float, float, float]:
	r, p = pearson_r(x, y)
	return r, pow(r, 2), p


def read_scores_from_file(file_name: str) -> Dict[str, float]:
	scores_dict = dict()
	with open(file_name, "r", encoding=UTF_8) as scores_file:
		for i, line in enumerate(scores_file):
			if i == 0:  # skip the header row
				continue
			line_split = line.strip().split(",")
			word = line_split[0]
			score = float(line_split[1])
			scores_dict[word] = score
	return scores_dict


if __name__ == "__main__":
	ensure_dir(OUTPUT_DIR)
	all_lemmas_set = set()
	all_lemmas = list()
	all_automated_scores = list()
	all_manual_scores = list()
	for group in LEMMA_GROUPS_LIST:
		# read scores from automated analysis
		automated_scores_file_name = get_search_results_file_name(group)
		automated_scores = read_scores_from_file(automated_scores_file_name)
		automated_scores_list = list()
		# read scores from manual analysis
		manual_scores_file_name = get_manual_scores_file_name(group)
		manual_scores = read_scores_from_file(manual_scores_file_name)
		manual_scores_list = list()
		# print paired scores into the individual output file, and put scores into all_lemmas, all_automated_scores, all_manual_scores
		output_file_name = OUTPUT_FILE_NAME_F.format(group)
		with open(output_file_name, "w", encoding=UTF_8) as output_file:
			print("lemma,automated score,manual score", file=output_file)
			for lemma, automated_score in automated_scores.items():
				if lemma not in manual_scores:
					raise ValueError(f"lemma {lemma} was found in the automated scores but not manual scores (group {group})")
				manual_score = manual_scores[lemma]
				automated_scores_list.append(automated_score)
				manual_scores_list.append(manual_score)
				print(f"{lemma},{automated_score},{manual_score}", file=output_file)
				if lemma not in all_lemmas_set:  # don't duplicate lemmas in the combined list
					all_lemmas_set.add(lemma)
					all_lemmas.append(lemma)
					all_automated_scores.append(automated_score)
					all_manual_scores.append(manual_score)
			for lemma in manual_scores:
				if lemma not in automated_scores:
					raise ValueError(f"lemma {lemma} was found in the manual scores but not automated scores (group {group})")
		# calculate correlation stuff for this group so it can be double checked against Excel's results
		r_value, r_squared, p_value = calculate_correlation(automated_scores_list, manual_scores_list)
		print(f"Group: {group}")
		print(f"n: {len(automated_scores_list)}")
		print(f"r: {r_value}")
		print(f"r^2: {r_squared}")
		print(f"p: {p_value}")
		print("----------")
	# print the combined data to a separate file
	combined_output_file_name = OUTPUT_FILE_NAME_F.format("COMBINED")
	with open(combined_output_file_name, "w", encoding=UTF_8) as output_file:
		print("lemma,automated score,manual score", file=output_file)
		for lemma, automated_score, manual_score in zip(all_lemmas, all_automated_scores, all_manual_scores):
			print(f"{lemma},{automated_score},{manual_score}", file=output_file)
	# calculate correlation stuff for the combined group so it can be double checked against Excel's results
	r_value, r_squared, p_value = calculate_correlation(all_automated_scores, all_manual_scores)
	print(f"Group: COMBINED")
	print(f"n: {len(all_automated_scores)}")
	print(f"r: {r_value}")
	print(f"r^2: {r_squared}")
	print(f"p: {p_value}")
	print("----------")
