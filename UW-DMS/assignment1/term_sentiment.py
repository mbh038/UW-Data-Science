# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 04:12:06 2015

@author: Mike

Term sentiment
"""

import sys
import json

def main():
    afinnfile = open(sys.argv[1])
    #afinnfile = open("AFINN-111.txt")
    tweetfile = open(sys.argv[2])
    #tweetfile = open("output.txt","r")
   
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    scorewords=scores.keys()

    tweetscore=[]
    otherword={}
    count=0
    for line in tweetfile:
        line_object = json.loads(line)
        try:
            tweetscore.append(0)
            #line=json.loads(line)
            tweetwords=line_object['text'].split()
            for word in tweetwords:
                if word in scorewords:
                    tweetscore[count]+=scores[word]
                else:
                    pass
            for word in tweetwords:
                if word not in scorewords:
                    #print word
                    if word in otherword:
                        otherword[word][0]+=1
                        otherword[word][1]+=tweetscore[count]
                    else:
                        otherword[word]=[1,tweetscore[count]]                     
        except:
            pass

        count+=1
#        if count > 100:
#            break
        
    for word in otherword:
        print word," ",otherword[word][1]/float(otherword[word][0])

if __name__ == '__main__':
    main()
    
