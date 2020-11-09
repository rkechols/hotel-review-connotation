UTF_8 = "utf8"
TXT_FILE_NAME_F = "./data/tripadvisor_{}-star.txt"
SPACY_ENGLISH_NAME = "en"


def get_rating_level_file_name(rating_level: int) -> str:
	return TXT_FILE_NAME_F.format(rating_level)
