import sys
import operator
import json
import random
import string
from collections import defaultdict

input = sys.argv[1]
model = sys.argv[2]

# Averaged Perceptron classifier

weight=defaultdict(float)
av_weight=defaultdict(float)
count=0

input_file=open(input,'r',errors='ignore')
# find the number of classes
total_class=[]
for sen in input_file:
    cl=sen.split()[0]
    total_class.append(cl)

Class=set(total_class)
length=len(Class)

rank={}
n=0
for i in Class:
    rank[i]=n
    n+=1

input_file=open(input,'r',errors='ignore')
for sen in input_file:
    words=sen.split()

    for word in words:
        if word not in weight:
           weight[word]=[0]*length
           av_weight[word]=[0]*length
        

# averaged perception
c=1

for t in range(5): # here change the iteration 
  input_file=open(input,'r',errors='ignore').readlines()
  sum_line=len(input_file)
  r_read=random.sample(range(sum_line),sum_line)

  for r_r in r_read:
  
    sen=input_file[r_r]
    words=sen.split()
    cl=words[0]
    r_cl=rank[cl]
    judge=defaultdict(float)

    for i in range(1,len(words)):    
        word=words[i]
        for cl1 in Class:
            r_cl1=rank[cl1]
            if word in weight:
               judge[cl1]+=weight[word][r_cl1]
            if word not in weight:
               print(word)

    if max(judge, key=judge.get)!= cl:
       for word in sen.split():
            if word not in Class:
                
                for cl1 in Class:
                    r_cl1=rank[cl1]	
                    if cl1 == cl:
                       weight[word][r_cl1]+=1
                       av_weight[word][r_cl1]+=c
                    if cl1 != cl:
                       weight[word][r_cl1]-=1
                       av_weight[word][r_cl1]-=c
                      
   	    	
    c+=1

for word in av_weight:
    for cl3 in Class:
        r_cl3=rank[cl3]
        av_weight[word][r_cl3]=weight[word][r_cl3]-av_weight[word][r_cl3]/float(c)

av_weight['N_rank']=rank

json.dump(av_weight,open(model,'w'))
