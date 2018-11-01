import numpy as np
import pandas as pd
import re
import nltk

#Inputing data 
#**********************************************************

data1 = pd.read_csv('processedSEQ.IN',header=None)
data2 = pd.read_csv('processedSEQ.OUT',header= None)

count =0

for counter in range(len(data1)):
	temp1 = data1.loc[counter].values[0].split()
	temp2 = data2.loc[counter].values[0].split()
	if(len(temp1) != len(temp2)):
		count = count + 1

print(count)			
#**********************************************************
			
