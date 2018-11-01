import nltk
from nltk.corpus import wordnet
import itertools
import pandas as pd
from pywsd.similarity import max_similarity as maxsim
from pywsd import disambiguate
import random

open("dissimilar_in",'w').close()
open("dissimilar_out",'w').close()
open("dissimilar_label",'w').close()
	

def generateSentence(line):
	prefix=[]
	suffix=[]
	if(type(line[0])==type("a")):
		prefix=[line[0]]
	else:
		#prefix=list(line[0])
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
	
				
def generateSentence2(line,token,slot_reference):
	reference =[]
	reply= []
	for i in token:
		reference.append(i[0])
	print("REF:",reference)
	print("LINE:",line)		
	for i in range(len(line)):
		current = line[i]
		if(isinstance(current, set)  and slot_reference[i] == "O"):
			for each in  current:
				temp = reference[i]
				reference[i]= "((__))".join(each.split())
				sentence = ""
				for a in reference:
					sentence = sentence + " "+  a
				reply.append(sentence)
				reference[i]=temp
	return reply 

def generateSimilarWordsFromSysnet(word,sysnet):
	synonyms = []
	antonyms = []
	for syn in wordnet.synsets(word):
		if(syn == sysnet):
			for l in syn.lemmas():
				synonyms.append(l.name().replace("_"," "))
				antonyms.append("not " +  (l.name().replace("_"," ")))
			if l.antonyms():
				antonyms.append(l.antonyms()[0].name())
	if(len(synonyms)<1):
		synonyms=[word]
	print("DISSIMILAR",antonyms)
	print("SIMILAR", synonyms)
	return set(synonyms),set(antonyms)


def createSimilaritySentences(sentence,slot_reference):
	tokenization = disambiguate(sentence)
	#######TMEP

	print(sentence)
	print(tokenization,len(tokenization))
	print(slot_reference,len(slot_reference))

	#######TMEP
		


	if(len(tokenization) !=len(slot_reference)):
		print(sentence)
		print(tokenization,len(tokenization))
		print(slot_reference,len(slot_reference))
		 
	longList_sim=[]
	longList_dis=[]
	for i in range(len(tokenization)):
		current= tokenization[i]
		if(slot_reference[i]!='O'):
			longList_sim.append(current[0]);
			longList_dis.append(current[0]);
			continue
		if(current[-1] is None):
			longList_sim.append(current[0])
			longList_dis.append(current[0])
			continue
		else:
			a,b = generateSimilarWordsFromSysnet(current[0],current[-1])
			longList_sim.append(a)
			longList_dis.append(b)
			continue
	reply = set(generateSentence(longList_sim))
	print(reply)
	print("DISSIM",longList_dis)

	dissimilar = generateSentence2(longList_dis,tokenization,slot_reference)
	answer = []
	for each in reply:
		sequence = []
		slot= []
		newSentence = each.split()
		for i in range(len(newSentence)):
			if(len(newSentence) != len(slot_reference)):
				print(sentence,longList_sim)
				print(newSentence, len(newSentence))
				print(slot_reference, len(slot_reference))
		
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
	answer2 = []
	for each in dissimilar:
		sequence = []
		slot= []
		newSentence = each.split()
		for i in range(len(newSentence)):
			if(len(newSentence) != len(slot_reference)):
				print(sentence,longList_sim)
				print(newSentence, len(newSentence))
				print(slot_reference, len(slot_reference))
		
			words=newSentence[i]
			length = len(words.split("((__))"))
			if(length<2):
				sequence.append(words)
				slot.append(slot_reference[i])
			else:
				for word in words.split(("((__))")):
					 sequence.append(word)
					 slot.append(slot_reference[i])
		answer2.append((sequence,slot))
	print(answer2)
	writeInFile(answer2)
	return answer


def writeInFile(list):
	file1 = open("dissimilar_in",'a')
	file2 = open("dissimilar_out",'a')
	file3 = open("dissimilar_label",'a')
	for each in list:
		file1.write(" ".join(each[0]))
		file2.write(" ".join(each[1]))
		file3.write("fallback")

		file1.write("\n")
		file2.write("\n")
		file3.write("\n")
	
	file1.close()
	file2.close()
	file3.close()
		

if __name__ == "__main__":
	#Inputing data
	#***********:***********************************************
	
	data1 = pd.read_csv('processedSEQ.IN',header=None)
	data2 = pd.read_csv('processedSEQ.OUT',header= None)
	data3 = pd.read_csv('label', header= None)
	data = [data1, data2, data3]
	file1 = open("ExtendedSeq.in","w") 
	file2 = open("ExtendedSeq.out","w") 
	file3 = open("ExtendedLabel","w") 

	data=pd.concat(data,axis=1)
	counting =0
	for  i in range(len(data)):
		da= createSimilaritySentences(data.loc[[i]].values[0][0], data.loc[[i]].values[0][1].split())
		for each in da:
			print(i)
			file1.write(" ".join(each[0]))
			file1.write("\n")
			file2.write(" ".join(each[1]))
			file2.write("\n")
			file3.write(data.loc[[i]].values[0][2])
			file3.write("\n")
	#**********************************************************i
	file1.close()
	file2.close()
	file3.close()

def DataExtraction(scale):
	#Inputing data
	#**********************************************************
	intent_data= os.path.join("./temp","processedSEQ.IN")	
	slot_data= os.path.join("./temp","processedSEQ.OUT")	
	label_data= os.path.join("./temp","processedLabel")	
	data1 = pd.read_csv(intent_data,header=None)
	data2 = pd.read_csv(slot_data,header= None)
	data3 = pd.read_csv(label_data, header= None)
	data = [data1, data2, data3]
	intent_loc= os.path.join("./temp/data","ExtendedSEQ.IN")	
	slot_loc= os.path.join("./temp/data","ExtendedSEQ.OUT")	
	label_loc= os.path.join("./temp/data","ExtendedLabel")	
	file1 = open(intent_loc,"w") 
	file2 = open(slot_loc,"w") 
	file3 = open(label_loc,"w") 
	data=pd.concat(data,axis=1)
	counting =0
	for  i in range(len(data)):
		da= createSimilaritySentences(data.loc[[i]].values[0][0], data.loc[[i]].values[0][1].split())
		file1.write(data.loc[[i]].values[0][0])
		file1.write("\n")
		file2.write(data.loc[[i]].values[0][1])
		file2.write("\n")
		file3.write(data.loc[[i]].values[0][2])
		file3.write("\n")
		if(scale<1):
			continue
		if(len(da)>scale):
			rndm = random.sample(range(1,len(da)-1), (scale-1)) 		
			for each in rndm:
				file1.write(" ".join(da[each][0]))
				file1.write("\n")
				file2.write(" ".join(da[each][1]))
				file2.write("\n")
				file3.write(data.loc[[i]].values[0][2])
				file3.write("\n")
		else:
			for each in da:
				file1.write(" ".join(each[0]))
				file1.write("\n")
				file2.write(" ".join(each[1]))
				file2.write("\n")
				file3.write(data.loc[[i]].values[0][2])
				file3.write("\n")
	file1.close()
	file2.close()
	file3.close()

