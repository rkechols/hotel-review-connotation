import os
import re
from util import get_rating_level_file_name, SPLIT_DIR, UTF_8


CSV_FILE_NAME = "./data/tripadvisor_hotel_reviews.csv"
DEAD_LINES_FILE_NAME = "dead_lines.csv"
CSV_LINE_RE = re.compile(r"\"(.*)\",([0-9])")
WHITESPACE_RE = re.compile(r"\s+")


if __name__ == "__main__":
	if not os.path.isdir(SPLIT_DIR):
		os.mkdir(SPLIT_DIR)
	if os.path.isfile(DEAD_LINES_FILE_NAME):
		os.remove(DEAD_LINES_FILE_NAME)
	output_files = dict()
	# noinspection PyBroadException
	try:
		for i in range(5):
			num_stars = i + 1
			txt_file_name = get_rating_level_file_name(num_stars)
			if os.path.isfile(txt_file_name):
				os.remove(txt_file_name)
			output_files[num_stars] = open(txt_file_name, "w", encoding=UTF_8)
		with open(CSV_FILE_NAME, "r", encoding=UTF_8) as csv_file:
			for line_num, line_ in enumerate(csv_file, start=1):
				if line_num == 1:  # skip the header row
					continue
				line = line_.strip()
				match = CSV_LINE_RE.match(line_)
				if match is None:
					print(f"{line_num},{line}", file=open(DEAD_LINES_FILE_NAME, "a", encoding=UTF_8))
				text = match.group(1)
				num_stars = int(match.group(2))
				if num_stars not in output_files:
					output_files[num_stars] = open(get_rating_level_file_name(num_stars), "w", encoding=UTF_8)
					print(f"unexpected number of stars {num_stars} found on line {line_num}")
				text = re.sub(WHITESPACE_RE, " ", text.strip())  # turn any whitespace into a single space
				print(text, file=output_files[num_stars])
	except Exception as e:
		print(f"exception of class {e.__class__.__name__}: {e}")
		for _, file in output_files.items():
			file.close()
