import json as js

class Text():
	"The class the bot use to process text..."

	def __init__(self):
		self.config = js.load(open("alphabets.json"))
		self.digits = self.config["digits"].split(",")
		self.alpha_caesar_es = self.config["caesar_es"].split(",")
		self.alpha_caesar_en = self.config["caesar_en"].split(",")
		
	def caesar_cypher(self, key, nkey, message, language):
		msg = message.upper()
		encrypted = ""
		n = 0
		if language == 0:
			alphabet = self.alpha_caesar_es
		elif language == 1:
			alphabet = self.alpha_caesar_en
		for c in msg:
			success, i = self.get_alphabet_index(c, alphabet)
			if success:
				encrypted += alphabet[(i+key)%len(alphabet)]
			else:
				success, i = self.get_alphabet_index(c, self.digits)
				if success:
					encrypted += self.digits[(i+nkey)%len(self.digits)]
				else:
					encrypted += c
		return encrypted
	
	def caesar_decypher(self, key, nkey, message, language):
		if language == 0:
			dkey = len(self.alpha_caesar_es) - key%27
		elif language == 1:
			dkey = len(self.alpha_caesar_en) - key%26
		return self.caesar_cypher(dkey, 10 - nkey%10, message, language)

	def get_alphabet_index(self, symbol, alphabet):
		n = 0
		success = False
		for a in alphabet:
			if symbol == a:
				success = True
				break
			else:
				n += 1
		return success, n