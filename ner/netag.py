import sys
import operator
import codecs
import json
import random
import string
from collections import defaultdict
from itertools import chain

def perceptron(files,t):

    weight=defaultdict(float)
    av_weight=defaultdict(float)
    count=0

    input_file=files.split('\n')
# find the number of classes
    total_class=[]
    for sen in input_file:
        if sen!='':
           cl=sen.split()[0]
           total_class.append(cl)

    Class=set(total_class)
    length=len(Class)

    rank={}
    n=0
    for i in Class:
        rank[i]=n
        n+=1

#Class=('HAM','SPAM')


    for sen in input_file:
        words=sen.split()

        for word in words:
            if word not in weight:
               weight[word]=[0]*length
               av_weight[word]=[0]*length
        

# averaged perception
    c=1

    for x in range(t):
        sum_line=len(input_file)
        r_read=random.sample(range(sum_line),sum_line)

        for r_r in r_read:
  
            sen=input_file[r_r]
            if sen !='':
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

               z=0
               for i in judge:
                   z+=judge[i]
               if z==0:
                   judge['SPAM']=1

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

    return av_weight


# function to split word
def divide(word):
    token=word.split('/')
    t={}
    t[1]=token[len(token)-1]
    t[0]=str.join('/',(token[i] for i in range(len(token)-1)))     
    return t


# function to judge the shape of words

pun=set(string.punctuation)
def word_type(word):
    buf=''
    for w in word:
        if w.isupper():
           if buf[-1:]!='A':
              buf+='A'
        if w.islower():
           if buf[-1:]!='a':
              buf+='a'
        if w in '0123456789':
           if buf[-1:]!='9':
              buf+='9'
        if w in pun:
           if buf[-1:]!='-':
              buf+='-'
    return buf

# function to judge special case

def special(word):

    if word[-2:]=='AQ' and word_type(word)=='Aa-A':
       return 'B-PER'
    if word[-3:]=='VMN' and word_type(word)=='Aa-A':
       return 'B-PER'
    if word[-3:]=='VMM' and word_type(word)=='Aa-A':
       return 'B-LOC'
    if word[-3:]=='VMI' and word_type(word)=='Aa-A':
       return 'B-ORG'
    if word[-2:]=='NP' and word_type(word)=='Aa-A':
       return 'B-PER'
    if word[-2:]=='NC' and word_type(word)=='Aa-A':
       return 'B-PER'
    if word_type(word)=='Aa-a-A' or word_type(word)=='A9-A':
       return 'B-MISC'
    else:
       return 'O'

###############################################################

sys.stdin=codecs.getreader('utf8')(sys.stdin.detach(),errors='ignore')
model = sys.argv[1]

weight=json.load(open(model))
instance=weight['Instance_More']
dic_one=weight['dic_one']
dic_more=perceptron(instance,5)
rank=dic_more['N_rank']

count=0
num=0
count3=0

for sen in sys.stdin:
  #  new_sen='H_prev '+sen+' H_end'

    words=sen.split()
    words.insert(0,words[len(words)-1])
    words.insert(len(words),words[1])
    tagger=defaultdict()

    tagger[0]='O'
    for i in range(1,len(words)-1):
        num+=1
      
        token=words[i]

        if token in dic_one:
           tagger[i]=dic_one[token]
           
        if words[i][0]=='/':
           #count3+=1
           tagger[i]='O'

        if token not in dic_one and words[i][0]!='/':
           token_p1=words[i-1]
           token_a1=words[i+1]

           judge=defaultdict(float)
           
           p_w='p:'+token_p1
           c_w='c:'+token
           n_w='n:'+token_a1  
           p_t=token+':'+tagger[i-1]

           dic_buffer={}
           dic_buffer[p_w]=0
           dic_buffer[c_w]=0
           dic_buffer[n_w]=0
           dic_buffer[p_t]=0

           for b in dic_buffer:
               if b in dic_more:
                  for c in rank:
                      r_c=rank[c]
                      judge[c]+=dic_more[b][r_c]
           if judge:
              tagger[i]=max(judge, key=judge.get)
           else:
              tagger[i]=special(token)
        if token not in dic_one and c_w not in dic_more:
           if tagger[i-1][0]=='B' or tagger[i-1][0]=='I':
              if word_type(token)=='Aa-A':
                 if token[-2:]=='NC' or token[-2:]=='AQ' or token[-3:]=='VMN' or token[-3:]=='VMM' or token[-3:]=='VMI' or token[-2:]=='NP': 
                    tagger[i]='I'+tagger[i-1][1:]
              else:
                 tagger[i]='O'
           if tagger[i-1][0]=='O':
              tagger[i]=special(token)


        sys.stdout.write(words[i])
        sys.stdout.write('/')
        sys.stdout.write(tagger[i])
        sys.stdout.write(' ')
        sys.stdout.flush()
        if i==len(words)-2:
           sys.stdout.write('\n')

