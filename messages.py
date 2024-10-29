import json as js
import random as rd

class Messages():
	"The class the bot use to know what to say..."

	def __init__(self):
		self.msg_es = js.load(open("assets/text/es/messages.json"))
		self.msg_en = js.load(open("assets/text/en/messages.json"))
		self.r_conversation_start_es = open("assets/text/es/random_conversation_start.txt").readlines()
		self.r_conversation_start_en = open("assets/text/en/random_conversation_start.txt").readlines()
		self.r_conversation_end_es = open("assets/text/es/random_conversation_end.txt").readlines()
		self.r_conversation_end_en = open("assets/text/en/random_conversation_end.txt").readlines()
		self.r_error_message_es = open("assets/text/es/random_apologies.txt").readlines()
		self.r_error_message_en = open("assets/text/en/random_apologies.txt").readlines()
		self.r_outofcontext_es = open("assets/text/es/random_outofcontext.txt").readlines()
		self.r_outofcontext_en = open("assets/text/en/random_outofcontext.txt").readlines()

	def get_message(self, key, l):
		if l == 1:
			return self.msg_en[key]
		else:
			return self.msg_es[key]

	def get_conversation_start(self, l):
		if l == 0:
			return rd.choice(self.r_conversation_start_es)
		else:
			return rd.choice(self.r_conversation_start_en)
	
	def get_conversation_end(self, l):
		if l == 0:
			return rd.choice(self.r_conversation_end_es)
		else:
			return rd.choice(self.r_conversation_end_en)
	
	def get_apology(self, l):
		if l == 0:
			return rd.choice(self.r_error_message_es)
		else:
			return rd.choice(self.r_error_message_en)
	
	def get_outofcontext(self, l):
		if l == 0:
			return rd.choice(self.r_outofcontext_es)
		else:
			return rd.choice(self.r_outofcontext_en)

	def levenshtein_distance_message(self, word_a, word_b, d, l):
		m = ""
		if l == 0:
			m += "La distancia de Levenshtein entre <b>" + word_a.upper() + "</b> y <b>"
			m += word_b.upper() + "</b> es <b>" + str(d) + "</b>."
		else:
			m += "The Levenshtein distance between <b>" + word_a.upper() + "</b> y <b>"
			m += word_b.upper() + "</b> is <b>" + str(d) + "</b>."
		return m

	def levenshtein_analysis_message(self, words, analysis, l):
		m = ""
		if l == 0:
			m += "Comparto mi análisis en una tabla:\n\n"
		else:
			m += "I share my analysis in the next table:\n\n"
		for w, a in zip(words, analysis):
			m += "<b>" + w.upper() + "</b>: "
			m += str(a[0]) + ", "
			m += str(a[1]) + ", "
			m += str(a[2]) + "\n"
		return m
	
	def __str__(self):
		return "- CryptoEX Bot\n" + \
				"  I am the class in charge of working with text messages...\n" + \
				"  gitlab.com/rodrigovalla/cryptoex_bot\n" + \
				"  rodrigovalla@protonmail.ch"
