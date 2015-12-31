# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 04:12:06 2015

@author: Mike

Tweet sentiment
"""

import sys
import json

def hw():
    print 'Hello, world!'

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
    count=0
    for line in tweetfile:
        line_object = json.loads(line)
        try:
            tweetscore.append(0)
            line=json.loads(line)
            tweetwords=line_object['text'].split()
            for word in tweetwords:
                if word in scorewords:
                    tweetscore[count]+=scores[word]
        except:
            tweetscore[count]=0
        print tweetscore[count]
        count+=1
    
if __name__ == '__main__':
    main()
