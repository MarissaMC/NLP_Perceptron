import sys
import json
import codecs
from collections import defaultdict

model = sys.argv[1]

av_weight=json.load(open(model))
rank=av_weight['N_rank']

Class=[]
for key in rank:
    Class.append(key)

#print(Class)
sys.stdin=codecs.getreader('utf8')(sys.stdin.detach(),errors='ignore')
for sen in sys.stdin:
    judge=defaultdict(float)
    for word in sen.split():
        if word in av_weight:
          # print(av_weight)
           for c in Class:
               r_c=rank[c]
               judge[c]+=av_weight[word][r_c]
      
    sys.stdout.write(max(judge, key=judge.get))
    sys.stdout.write('\n')
 
