import sys
import json
import re, string
import codecs
from collections import defaultdict

input=sys.argv[1]
model=sys.argv[2]

# weight
dic_one = defaultdict()
dic_more = defaultdict()
weight = defaultdict()
instance=''
# function to split word
def divide(word):
    token=word.split('/')
    t={}
    t[1]=token[len(token)-1]
    t[0]=str.join('/',(token[i] for i in range(len(token)-1)))     
    return t

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

f=codecs.open(input,'r',"Latin-1",errors='ignore')
#with open(input,'r',errors='ignore') as f:
for line in f:
        for word in line.split():
            token=word.split('/')
            if len(token)>2:
               token=divide(word)
           
            if token[0] not in dic_more:
               if token[0] not in dic_one:
                  dic_one[token[0]]=token[1]

               if dic_one[token[0]]!=token[1]:
                  dic_more[token[0]]={}
                  dic_more[token[0]][dic_one[token[0]]]=0
                  dic_more[token[0]][token[1]]=0
                  del dic_one[token[0]]

            if token[0] in dic_more:
               if token[1] not in dic_more[token[0]]:               
                  dic_more[token[0]][token[1]]=0

f=codecs.open(input,'r',"Latin-1",errors='ignore')
#with open(input,'r',errors='ignore') as f:
for line in f:

        words=line.split()
        words.insert(0,words[len(words)-1])
        words.insert(0,words[len(words)-2])
        words.insert(len(words),words[2])

        for i in range(2,len(words)-1):

            token=divide(words[i])

            if token[0] not in dic_one:

               token_p1=divide(words[i-1])
               token_p2=divide(words[i-2])
               token_a1=divide(words[i+1])


               tag=token[1]
               p2_tag='p2:'+token[0]+token_p2[1]
               p2_word='p2:'+token[0]+token_p2[0]
               p_word='p:'+token[0]+token_p1[0]
               c_word='c:'+token[0]
               n_word='n:'+token[0]+token_a1[0]
               p_tag='p1:'+token[0]+token_p1[1]
               p_2tag=token[0]+token_p1[1]+token_p2[1]


               instance+=(tag)
               instance+=(' ')               
               instance+=(p_word)
               instance+=(' ')     
               instance+=(p2_word)
               instance+=(' ')           
               instance+=(c_word)
               instance+=(' ')               
               instance+=(n_word)
               instance+=(' ')               
               instance+=(p_tag)
               instance+=(' ')
               instance+=(p2_tag)
               instance+=(' ') 
               instance+=(p_2tag)
               instance+=(' ')
               instance+=('')
               instance+=('\n')   

weight['Instance_More']=instance   
weight['dic_one']=dic_one

w_file=codecs.open(model,'w',"Latin-1")
#w_file.write(instance)  
json.dump(weight, w_file,ensure_ascii=False)
