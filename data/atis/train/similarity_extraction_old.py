import nltk
from nltk.corpus import wordnet
import itertools
import pandas as pd

from pywsd.similarity import max_similarity as maxsim
from pywsd import disambiguate



def createSimilarSentences(utterance, slot_reference):
	utterance_tokenization = nltk.word_tokenize(utterance)
	utterance_POS = nltk.pos_tag(utterance_tokenization)
	print(utterance_POS)

def abc():
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
			print("NN",POS_token[0],POS_token[1])
			longList.append(POS_token[0])
	
		elif (POS_token[1].startswith("VB")):
			print("VBP WAS HERE")
			postion.add(count)
			verb.append(POS_token[0])
			longList.append(getSimilarWords(POS_token[0]))
		else:
			print("HI")
			longList.append(POS_token[0]);
		count+=1
	print(longList)
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
	

def generateSentence2(line):
	prefix=[]
	suffix=[]
	if(type(line[0])==type("a")):
		prefix=[line[0]]
	else:
		prefix=list(line[0])
		for words in line[0]:
			if(len(words.split())>1):
				words= "((__))".join(words.split())
			prefix.append(words)
	
	sentences=set()
	for i in range(1,len(line)):
		if(type(line[i])==type("a")):
			suffix=[line[i]]
		else:
			suffix=[]
			for words in line[i]:
				if(len(words.split())>1):
					words= "((__))".join(words.split())
				suffix.append(words)
		prefix=[name1+" "+name2 for name1 in prefix for name2 in suffix]
	return prefix
	
				
	

def generateSimilarWordsFromSysnet(word,sysnet):
	synonyms = []
	for syn in wordnet.synsets(word):
		if(syn == sysnet):
			for l in syn.lemmas():
				print(l)
				synonyms.append(l.name().replace("_"," "))
	if(len(synonyms)<1):
		synonyms=[word]
	return set(synonyms)


def getSimilarWords(word,type):
	synonyms = []
	for syn in wordnet.synsets(word):
		print("--------------------")
		print(syn)
		for l in syn.lemmas():
			print(l)
			synonyms.append(l.name().replace("_"," "))
	if(len(synonyms)<1):
		synonyms=[word]
	return set(synonyms)

if __name__ == "__main__":
	#Inputing data
	#**********************************************************
	
	data1 = pd.read_csv('processedSEQ.IN',header=None)
	data2 = pd.read_csv('processedSEQ.OUT',header= None)
	data3 = pd.read_csv('label', header= None)
	data = [data1, data2, data3]
	data=pd.concat(data,axis=1)
	counting =0
	for  i in range(len(data)):
		(createSimilarSentences(data.loc[[i]].values[0][0], data.loc[[i]].values[0][1].split()))
		print(counting,"  888888888888888888888888888888888888888888")
		break	
	#**********************************************************i
	print(counting)


def getSimilaritySentences2(sentence,slot_reference):
	tokenization = disambiguate(sentence) 
	longList=[]
	for i in range(len(tokenization)):
		current= tokenization[i]
		if(slot_reference[i]!='O'):
			longList.append(current[0]);
			continue
		if(current[-1] is None):
			longList.append(current[0])
			continue
		else:
			longList.append(generateSimilarWordsFromSysnet(current[0],current[-1]))
			continue
	print("LongList",longList)
	reply = set(generateSentence2(longList))
	answer = []
	for each in reply:
		sequence = []
		slot= []
		newSentence = each.split()
		for i in range(len(newSentence)):
			words=newSentence[i]
			length = len(words.split("((__))"))
			if(length<2):
				sequence.append(words)
				slot.append(slot_reference[i])
			else:
				for word in words.split(("((__))")):
					 sequence.append(word)
					 slot.append(slot_reference[i])
		answer.append((sequence,slot))
	return answer
