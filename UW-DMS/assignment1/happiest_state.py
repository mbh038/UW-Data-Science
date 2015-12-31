# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 08:42:36 2015

@author: Mike
"""

import sys
import json
import operator
  
def scoreWords(sentimentScoresFile):
    """
    sentimentScoresFile: a sentiment file of words with sentiment score,
    each line as word \t score.
    
    returns: sentimentScores{} a dictionary of word: score key:value pairs
    """
    sentimentScores = {} # initialize an empty dictionary
    for line in sentimentScoresFile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        sentimentScores[term] = int(score)  # Convert the score to an integer.
    return sentimentScores
    
def tweetScore(tweet,sentimentScores):
    """
    tweet: a tweet as one line of text
    scores: dictionary of "word":sentiment score pairs
    
    returns tweetscore (int) = sum of individual word scores in tweet text.
    """
    scorewords=sentimentScores.keys()
    score=0
    line_object=json.loads(tweet)
    tweetwords=line_object['text'].split()
    for word in tweetwords:
        if word in scorewords:
            score += sentimentScores[word]
    return score

def langTweets(tweetfile,languages):  # did not need this
    """
    tweetfile:file object that is text, each line a tweet structured as per twitter.
    languages: list of languages of tweets to be retained, using twitter abbreviations
    returns: file object of tweets in tweetfile, in selected languages only.
    """
    newText=""
    linesIn=0
    linesOut=0
    for line in tweetfile:
        line=line.rstrip()
        #line.strip('\r')
        linesIn+=1
        try:
           line_object = json.loads(line)
           tweetLang=line_object['lang']
           if tweetLang in languages:
               newText=newText+line+"\n"
               #print line
               linesOut+=1
        except:
            pass
    newText.rstrip("\n")
    #print linesIn,linesOut
    return newText
         

def main():
    
    afinnfile = open(sys.argv[1])
    #afinnfile = open("AFINN-111.txt")
    tweetfile = open(sys.argv[2])
    #tweetfile = open("output.txt","r")
 
    states=statesDict()
    sentimentScores=scoreWords(afinnfile)

    tweetNum=0

    tweet_states={}
    for line in tweetfile:       
        try:
            #print line
            line_object = json.loads(line)
            #print line_object          
            location_words=line_object['user']['location'].split()
            #print location_words
            tweet_score=tweetScore(line,sentimentScores)
            for word in location_words:
                    if word in states:
                        if word in tweet_states:
                            tweet_states[word][0]+=tweet_score
                            tweet_states[word][1]+=1
                        else:
                            tweet_states[word]=[tweet_score,1]
        except:
            pass
        tweetNum+=1
        
    #print tweet_states
    for state in tweet_states:
        tweet_states[state]=tweet_states[state][0]/float(tweet_states[state][1])
    #print tweet_states
    #print min (tweet_states.values()),max (tweet_states.values()),sum (tweet_states.values())
    happiest= max(tweet_states.iteritems(), key=operator.itemgetter(1))[0]
    print happiest
    
def statesDict():
    states = {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'
    }
    return states

if __name__ == '__main__':
    main()