class SimpleToken:
	def __init__(self, text: str, lemma: str, part_of_speech: str):
		self.text = text
		self.lemma = lemma
		self.part_of_speech = part_of_speech

	def __str__(self) -> str:
		return f"({self.text}, {self.lemma}, {self.part_of_speech})"

	def __repr__(self) -> str:
		return self.__str__()
