# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 04:12:06 2015

@author: Mike

Frequency
"""

import sys
import json

def main():

    tweetfile = open(sys.argv[1])
    #tweetfile = open("output.txt","r")

    terms={}           
    for line in tweetfile:
        line_object = json.loads(line)
        try:
            tweetwords=line_object['text'].split()
            for word in tweetwords:
                terms[word]=terms.get(word,0)+1
        except:
            pass

    total=0    
    for word in terms:
        total+=terms[word]
    for word in terms:
        print word," ",terms[word]/float(total)
  
if __name__ == '__main__':
    main()