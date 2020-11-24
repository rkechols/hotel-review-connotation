import numpy as np
from typing import List, Tuple
from simple_token import SimpleToken
from tokenize_english import read_tks_file
from util import get_tokenized_file_name, TOKENIZED_DIR
import matplotlib.pyplot as plt


def rating_level_stats(document: List[List[SimpleToken]], plot_title: str) -> Tuple[float, float, int]:
	counts = np.array([len(review) for review in document])
	max_count = np.amax(counts)
	if max_count % 100 != 0:
		max_count = 100 * (1 + (max_count // 100))  # round up to the nearest multiple of 100
	plt.hist(counts, bins=list(range(0, max_count + 1, 100 )))
	plt.title(plot_title)
	plt.xlabel("# of tokens")
	plt.show()
	average = np.mean(counts)
	standard_deviation = np.std(counts)
	median = np.median(counts)
	return float(average), float(standard_deviation), int(median)


if __name__ == "__main__":
	print(f"loading tokens from files in {TOKENIZED_DIR}")
	print("----------")
	all_documents = dict()
	for i in range(5):
		rating_level = i + 1
		doc = read_tks_file(get_tokenized_file_name(rating_level))
		avg, std, med = rating_level_stats(doc, f"{rating_level}-star reviews")
		print(f"{rating_level}-star reviews:\taverage token count = {avg}\tstandard deviation = {std}\tmedian = {med}")
		all_documents[rating_level] = doc
	all_reviews_smashed = list()
	for reviews in all_documents.values():
		all_reviews_smashed += reviews
	avg, std, med = rating_level_stats(all_reviews_smashed, "Histogram of tokens per review")
	print("----------")
	print(f"all reviews:\taverage token count = {avg}\tstandard deviation = {std}\tmedian = {med}")
	print("----------")
