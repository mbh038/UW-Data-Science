# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 08:42:36 2015

@author: Mike

Top_ten.py

Find the top ten most used hashtags in a twitter stream

See: https://dev.twitter.com/overview/api/tweets
"""

import sys
import json
import operator

def main():
    tweetfile = open(sys.argv[1])
    #tweetfile = open("output.txt","r")
    hashtaglist={} # will be key:hashtag, value: occurrences of hashtag
    for line in tweetfile:
        try:
            line_object = json.loads(line)
            hashtags=line_object['entities']['hashtags']
            for x in hashtags:
                hashtaglist[x['text']]=hashtaglist.get(x['text'],0)+1
        except:
            pass  
    
    # sort hashtaglist by occurrences
    # sorted_x will be a list of tuples sorted by the second element in each tuple.
    # got this from : Devin Jeanpierre @ http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
    sorted_x = sorted(hashtaglist.items(), key=operator.itemgetter(1))
    #get the top ten in descending order of number of occurrences
    top_ten = list(reversed(sorted_x[-10:]))
    for hashtag in top_ten:
        print hashtag[0]," ",hashtag[1]
        
if __name__ == '__main__':
    main()
    
    