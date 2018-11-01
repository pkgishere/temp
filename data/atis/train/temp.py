import nltk
from nltk.corpus import wordnet
import itertools

def createSimilarSentences(utterance, slot_reference):
	utterance_tokenization = nltk.word_tokenize(utterance)
	utterance_POS = nltk.pos_tag(utterance_tokenization)
	adj = []
	modal=[]
	noun=[]
	adverb=[]
	particle=[]
	verb=[]
	longList=[]
	#longListNeg=[]
	postion=set()
	count =0
	
	for i in range(len(utterance_POS)):
		POS_token = utterance_POS[i]
		if(slot_reference[i]!='O'):
			longList.append(POS_token[0]);
			continue
		if (POS_token[1].startswith("JJ")):
			postion.add(count)
			adj.append(POS_token[0])
			longList.append(getSimilarWords(POS_token[0]))
        		#    longListNeg.append(i[0])
		elif (POS_token[1].startswith("MD")):
			postion.add(count)
			modal.append(POS_token[0])
			longList.append(getSimilarWords(POS_token[0]));
           		 #longListNeg.append(i[0])
		elif (POS_token[1].startswith("RB")):
			postion.add(count)
			adverb.append(POS_token[0])
			longList.append(getSimilarWords(POS_token[0]));
			#longListNeg.append(i[0])
		elif (POS_token[1].startswith("RP")):
			postion.add(count)
			particle.append(POS_token[0])
			longList.append(getSimilarWords(POS_token[0]))
			#longListNeg.append(i[0])

		elif (POS_token[1].startswith("NN")):
			postion.add(count)
			noun.append(POS_token[0])
			longList.append(getSimilarWords(POS_token[0]))
        	#     longListNeg.append(i[0])
	
		elif (POS_token[1].startswith("VB")):
			postion.add(count)
			verb.append(POS_token[0])
			longList.append(getSimilarWords(POS_token[0]))
		else:
			longList.append(POS_token[0]);
		count+=1
	return set(generateSentence(longList))
	#return(generateSentence(longList))


def generateSentence(line):
	prefix=[]
	if(type(line[0])==type("a")):
		prefix=[line[0]]
	else:
		prefix=list(line[0])
		for words in line[0]:
			prefix.append(words)
	
	sentences=set()
	for i in range(1,len(line)):
		if(type(line[i])==type("a")):
			suffix=[line[i]]
		else:
			suffix=list(line[i])
		prefix=[name1+" "+name2 for name1 in prefix for name2 in suffix]
	return prefix
	

def getSimilarWords(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name().replace("_"," "))
    if(len(synonyms)<1):
        synonyms=[word]
    return set(synonyms)


