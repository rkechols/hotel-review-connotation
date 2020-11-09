from tokenize_english import get_all_tokenized_ratings


CONTEXT_FILE_NAME_F = "./data/contexts/{}_context_{}.txt"


def get_context_file_name(word: str, rating_level: int) -> str:
	return CONTEXT_FILE_NAME_F.format(word, rating_level)


if __name__ == "__main__":
	# tokenize files
	docs = get_all_tokenized_ratings()
	# find tokens in question
	# TODO
