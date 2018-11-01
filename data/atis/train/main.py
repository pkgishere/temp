import numpy as np
import pandas as pd
import re
import nltk

#Inputing data 
#**********************************************************

data1 = pd.read_csv('seq.in',header=None)
data2 = pd.read_csv('seq.out',header= None)
data3 = pd.read_csv('label', header= None)
data = [data1, data2, data3]
data=pd.concat(data,axis=1)
#**********************************************************



#Pre-processing
#**********************************************************

count =0
count2 =0
diff=0
def process(X, annotation,temp):
	inputLine=[]	
	annotatedLine=[]
	for  i in range(len(X)):
		wrd = X[i]
		wrd = wrd.replace(u'’', u"'")
		regexp1 = re.compile(r"([A-Za-z0-9])&([A-Za-z0-9])")
		regexp2 = re.compile(r"([A-Za-z0-9]):")
		regexp3 = re.compile(r"\'ll")
		regexp4 = re.compile(r"\'m")
		regexp5 = re.compile(r'can\'t')
		regexp6 = re.compile(r"won\'t")
		regexp7 = re.compile(r"n\'t")
		regexp8 = re.compile(r"\'re")
		regexp9 = re.compile(r"\'ve")
		regexp10 = re.compile(r"\'d")
		regexp11 = re.compile(r"\'t")
		regexp12 = re.compile(r"t's")
		regexp13 = re.compile(r"'s")

	
		if regexp1.search(wrd):
			wrd = re.sub(r"([A-Za-z0-9])&([A-Za-z0-9])", r"\1 and \2", wrd)
			for word in wrd.split():
				inputLine.append(word)
				annotatedLine.append(annotation[i])
		elif(regexp2.search(wrd)):
			wrd = re.sub(r"([A-Za-z0-9]):", r"\1 :", wrd)
			for word in wrd.split():
				inputLine.append(word)
				annotatedLine.append(annotation[i])
		elif(regexp3.search(wrd)):
			wrd = re.sub(r"\'ll", " will", wrd)
			for word in wrd.split():
				inputLine.append(word)
				annotatedLine.append(annotation[i])
		elif(regexp4.search(wrd)):
			wrd = re.sub(r"\'m", " am", wrd)
			for word in wrd.split():
				inputLine.append(word)
				annotatedLine.append(annotation[i])
		elif(regexp5.search(wrd)):
			wrd = re.sub(r"can\'t", "can not", wrd)
			for word in wrd.split():
				inputLine.append(word)
				annotatedLine.append(annotation[i])
		elif(regexp6.search(wrd)):
			wrd = re.sub(r"won\'t", "would not", wrd)
			for word in wrd.split():
				inputLine.append(word)
				annotatedLine.append(annotation[i])

		elif(regexp7.search(wrd)):
			wrd = re.sub(r"n't", "not", wrd)
			for word in wrd.split():
				inputLine.append(word)
				annotatedLine.append(annotation[i])
		elif(regexp8.search(wrd)):
			wrd = re.sub(r"\'re", " are", wrd)
			for word in wrd.split():
				inputLine.append(word)
				annotatedLine.append(annotation[i])
		elif(regexp9.search(wrd)):
			wrd = re.sub(r"\'ve", " have", wrd)
			for word in wrd.split():
				inputLine.append(word)
				annotatedLine.append(annotation[i])
		elif(regexp10.search(wrd)):
			wrd = re.sub(r"\'d", " had", wrd)
			for word in wrd.split():
				inputLine.append(word)
				annotatedLine.append(annotation[i])
		elif(regexp11.search(wrd)):
			wrd = re.sub(r"\'t", " not", wrd)
			for word in wrd.split():
				inputLine.append(word)
				annotatedLine.append(annotation[i])
		elif(regexp12.search(wrd)):
			wrd = re.sub(r"t's", "t is", wrd)
			for word in wrd.split():
				inputLine.append(word)
				annotatedLine.append(annotation[i])
		elif(regexp13.search(wrd)):
			wrd = re.sub(r"'s", "s", wrd)
			for word in wrd.split():
				inputLine.append(word)
				annotatedLine.append(annotation[i])
		else:
			inputLine.append(wrd)
			annotatedLine.append(annotation[i])
		
	return(inputLine,annotatedLine)




if __name__ == "__main__":
	file1 = open('processedSEQ.IN','w')
	file2 = open('processedSEQ.OUT','w')
	for counter in range(len(data1)):
		temp1 = nltk.word_tokenize(data1.loc[counter].values[0])
		temp2 = data1.loc[counter].values[0].split()
		if(len(temp1) != len(temp2)):
			temp2,temp3 =  process(data1.loc[counter].values[0].split(),data2.loc[counter].values[0].split(),counter)
			file1.write(" ".join(temp2))
			file2.write(" ".join(temp3))
		else:
			file1.write(data1.loc[counter].values[0])
			file2.write(data2.loc[counter].values[0])
		file1.write("\n")
		file2.write("\n")

	file1.close()
	file2.close()			
			
