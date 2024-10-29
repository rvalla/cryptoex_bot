import json as js

class Text():
	"The class the bot use to process text..."

	def __init__(self):
		self.config = js.load(open("alphabets.json"))
		self.digits = self.config["digits"].split(",")
		self.alpha_caesar_es = self.config["caesar_es"].split(",")
		self.alpha_caesar_en = self.config["caesar_en"].split(",")
		self.levenshtein = Levenshtein()
	
	#Encrypting and decrypting a message with Caesar cipher...
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
	
	def caesar_by_word_cypher(self, message, language):
		words = message.split(" ")
		encrypted = ""
		for w in words:
			encrypted += self.caesar_cypher(-len(w), -len(w), w, language)
			encrypted += " "
		return encrypted
	
	def caesar_by_word_decypher(self, message, language):
		words = message.split(" ")
		plain = ""
		for w in words:
			plain += self.caesar_decypher(-len(w), -len(w), w, language)
			plain += " "
		return plain
	
	#Encrypting and decrypting a message reversing symbol's order...
	def mirror_cypher(self, key, message):
		msg = message.replace(" ", "+")
		k = key.replace(" ", "+")
		m = self.mirror_string(k, msg.split(k))
		return m

	def mirror_string(self, key, links):
		m = ""
		for l in links:
			m += l[::-1]
			m += key
		return m[:len(m)-len(key)]
	
	def mirror_decypher(self, key, message):
		k = key.replace(" ", "+")
		m = self.mirror_string(key, message.split(k))
		return m.replace("+", " ")

	#Working with Levenshtein distance...
	def levenshtein_distance(self, word_a, word_b):
		return self.levenshtein.distance(word_a, word_b)

	def levenshtein_analysis(self, word_list):
		analysis = []
		for w in range(len(word_list)):
			analysis.append((len(word_list[w]),
							len(word_list[(w+1)%len(word_list)]) - len(word_list[w]),
							self.levenshtein_distance(word_list[w], word_list[(w+1)%len(word_list)])))
		return analysis

	def __str__(self):
		return "- CryptoEX Bot\n" + \
				"  I am the class in charge of encrypting and decrypting text...\n" + \
				"  gitlab.com/rodrigovalla/cryptoex_bot\n" + \
				"  rodrigovalla@protonmail.ch"


class Levenshtein():
    
    #Measuring Levenshtein distance dinamically...
    #https://en.wikipedia.org/wiki/Levenshtein_distance#Iterative_with_full_matrix
    def distance(self, word_a, word_b):
       m = self.compute_matrix(word_a, word_b, len(word_a), len(word_b))
       return m[len(m)-1][len(m[0])-1]

    #Getting details from a distance computation...
    def detailed_distance(self, word_a, word_b):
        m = self.compute_matrix(word_a, word_b, len(word_a), len(word_b))
        s = "Computing distance between " + word_a + " and " + word_b + ":\n\n"
        s += self.get_matrix_string(word_a, word_b, m)
        s += "\n\n"
        s += "Distance = " + str(m[len(m)-1][len(m[0])-1])
        return s

    #Building the matrix to compute Levenshtein distance between two words...
    def compute_matrix(self, word_a, word_b, a, b):
        #We create the matrix of len(word_a) + 1 rows and len(word_b) + 1 columns
        m = self.build_empty_matrix(a, b)
        
        #Now we compute Levenshtein distance between all prefixes...
        for r in range(a):
            for c in range(b):
                #We check if both characters are equal...
                x = 1
                if word_a[r] == word_b[c]:
                    x = 0
                m[r+1][c+1] = min([
                                m[r+1][c] + 1, #insertion vs deletion vs replacement
                                m[r][c+1] + 1,
                                m[r][c] + x
                            ])
        return m
    
    #Building an empty matrix to work with...
    def build_empty_matrix(self, a, b):
        m = [[n for n in range(b + 1)]]        
        for i in range (1, a + 1):
            m.append([0 for n in range(b+1)])
        for i in range(1,len(m)):
            m[i][0] = i
        return m
    
    def get_matrix_string(self, word_a, word_b, matrix):
        s = ""
        a = " " + word_a
        b = "  " + word_b
        for l in b:
            s += "  "
            s += l
            s += " "
        s += "\n"
        for r in range(len(matrix)):
            s += "  "
            s += a[r]
            s += " "
            for c in range(len(matrix[0])):
                s += " "
                if matrix[r][c] < 10:
                    s += " "
                s += str(matrix[r][c])
                s += " "
            s += "\n"
        return s   

    #Printing class information...
    def __str__(self):
        return "I am a class with the power of computing the Levenshtein distance between words!\n" + \
                "Because of that I know that the distance between 'matrix' and 'mattress' is 4."
