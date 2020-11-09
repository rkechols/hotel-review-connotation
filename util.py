UTF_8 = "utf8"
TXT_FILE_NAME_F = "data/split/tripadvisor_{}-star.txt"
SPACY_ENGLISH_NAME = "en"
TOKENIZED_DIR = "./data/tokenized/"
TOKENIZED_FILE_NAME_F = TOKENIZED_DIR + "{}-star-tokenized.tks"


def get_rating_level_file_name(rating_level: int) -> str:
	return TXT_FILE_NAME_F.format(rating_level)


def get_tokenized_file_name(rating_level: int) -> str:
	return TOKENIZED_FILE_NAME_F.format(rating_level)
