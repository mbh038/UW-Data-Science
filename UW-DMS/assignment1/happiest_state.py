# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 08:42:36 2015

@author: Mike
"""

import sys
import json
import operator
import math

def distance (lat1,lon1,lat2,lon2):
    
    lat1,lon1,lat2,lon2=math.radians(lat1),math.radians(lon1),math.radians(lat2),math.radians(lon2),
    a=6378.137 #km
    b = 6356.752 # km
    r = (1/float(3))*(2*a+b)
    
    dx=math.cos(lat2)*math.cos(lon2) - math.cos(lat1)*math.cos(lon1)
    dy=math.cos(lat2)*math.sin(lon2) - math.cos(lat1)*math.sin(lon1)
    dz=math.sin(lat2) - math.sin(lat1)
    C=(dx**2+dy**2+dz**2)**0.5

    dsigma=2*math.asin(C/2)
    
    dist= r * dsigma
    return dist
    
def findState (lat,lon):
    minDist=None
    nearest=None
    states=statesDict()
#    for state in states:
#        #print states[state][1],states[state][2]
    for state in states:
        dist=distance(lat,lon,states[state][1],states[state][2])
        if minDist == None or minDist>dist:
            minDist=dist
            nearest=state
    return nearest
  
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
         
def userLocate(sentimentFile,tweetFile):
    states=statesDict()
    sentimentScores=scoreWords(sentimentFile)
    tweetNum=0
    tweet_states={}
    for line in tweetFile: 
        try:
            line_object = json.loads(line)
            location_words=line_object['user']['location'].split()          
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
       
    return tweet_states
    
def coordLocate(sentimentFile,tweetFile):
#    states=statesDict()
    sentimentScores=scoreWords(sentimentFile)
    tweet_states={}
    for line in tweetFile: 
            try:
                line_object = json.loads(line)   
                coords=line_object['coordinates']['coordinates']
                #print coords
                tweet_score=tweetScore(line,sentimentScores)
                tweetState=findState(float(coords[0]),float(coords[1]))
                #print tweetState
                if tweetState in tweet_states:
                    tweet_states[tweetState][0]+=tweet_score
                    tweet_states[tweetState][1]+=1
                else:
                    tweet_states[tweetState]=[tweet_score,1]
            except:
                pass
    return tweet_states
    
def Locate(sentimentFile,tweetFile):
    states=statesDict()
    sentimentScores=scoreWords(sentimentFile)
    tweetNum=0
    tweet_states={}
    for line in tweetFile:       
        try:
            line_object = json.loads(line)
            location_words=line_object['user']['location'].split()
            tweet_score=tweetScore(line,sentimentScores)
            for word in location_words:
                    if word in states:
                        if word in tweet_states:
                            tweet_states[word][0]+=tweet_score
                            tweet_states[word][1]+=1
                        else:
                            tweet_states[word]=[tweet_score,1]    
        except:
            try:
                #line_object = json.loads(line)   
                coords=line_object['coordinates']['coordinates']
                #print coords
                tweet_score=tweetScore(line,sentimentScores)
                tweetState=findState(float(coords[0]),float(coords[1]))
                #print tweetState
                if tweetState in tweet_states:
                    tweet_states[tweetState][0]+=tweet_score
                    tweet_states[tweetState][1]+=1
                else:
                    tweet_states[tweetState]=[tweet_score,1]
            except:
                pass
            
    return tweet_states
    
def main():
    
    #afinnfile = open(sys.argv[1])
    afinnfile = open("AFINN-111.txt").readlines()
    #print len (afinnfile)
    #tweetfile = open(sys.argv[2])
    tweetfile = open("output.txt","r").readlines()
    #print len (tweetfile)
    #tweetfile=langTweets(tweetfile,["en"])
    tweet_states1=userLocate(afinnfile,tweetfile)
#    print tweet_states1
    for state in tweet_states1:
        tweet_states1[state]=tweet_states1[state][0]/float(tweet_states1[state][1])
    happiest= max(tweet_states1.iteritems(), key=operator.itemgetter(1))[0]
    #print happiest,len (tweet_states1)
    #print
    
    tweet_states2=coordLocate(afinnfile,tweetfile)     
    #print tweet_states2
#    for state in tweet_states2:
#        if state in tweet_states1:
#            print "Duplicate!"
    for state in tweet_states2:
        tweet_states2[state]=tweet_states2[state][0]/float(tweet_states2[state][1])
    happiest= max(tweet_states2.iteritems(), key=operator.itemgetter(1))[0]
   # print happiest,len (tweet_states2)
    
    tweet_states3=Locate(afinnfile,tweetfile)
    #print tweet_states3
    for state in tweet_states3:
        tweet_states3[state]=tweet_states3[state][0]/float(tweet_states3[state][1])
    happiest= max(tweet_states3.iteritems(), key=operator.itemgetter(1))[0]
    print happiest#,len (tweet_states3)
#    print
    
    
def statesDict():
    states={
    'AK':['Alaska',61.3850,-152.2683],
    'AL':['Alabama',32.7990,-86.8073],
    'AR':['Arkansas',34.9513,-92.3809],
    'AS':['American Samoa',14.2417,-170.7197],
    'AZ':['Arizona',33.7712,-111.3877],
    'CA':['California',36.1700,-119.7462],
    'CO':['Colorado',39.0646,-105.3272],
    'CT':['Connecticut',41.5834,-72.7622],
    'DC':['District of Columbia',38.8964,-77.0262],
    'DE':['Delaware',39.3498,-75.5148],
    'FL':['Florida',27.8333,-81.7170],
    'GA':['Georgia',32.9866,-83.6487],
    'HI':['Hawaii',21.1098,-157.5311],
    'IA':['Iowa',42.0046,-93.2140],
    'ID':['Idaho',44.2394,-114.5103],
    'IL':['Illinois',40.3363,-89.0022],
    'IN':['Indiana',39.8647,-86.2604],
    'KS':['Kansas',38.5111,-96.8005],
    'KY':['Kentucky',37.6690,-84.6514],
    'LA':['Louisiana',31.1801,-91.8749],
    'MA':['Massachusetts',42.2373,-71.5314],
    'MD':['Maryland',39.0724,-76.7902],
    'ME':['Maine',44.6074,-69.3977],
    'MI':['Michigan',43.3504,-84.5603],
    'MN':['Minnesota',45.7326,-93.9196],
    'MO':['Missouri',38.4623,-92.3020],
    'MP':['Northern Mariana Islands',14.8058,145.5505],
    'MS':['Mississippi',32.7673,-89.6812],
    'MT':['Montana',46.9048,-110.3261],
    'NC':['North Carolina',35.6411,-79.8431],
    'ND':['North Dakota',47.5362,-99.7930],
    'NE':['Nebraska',41.1289,-98.2883],
    'NH':['New Hampshire',43.4108,-71.5653],
    'NJ':['New Jersey',40.3140,-74.5089],
    'NM':['New Mexico',34.8375,-106.2371],
    'NV':['Nevada',38.4199,-117.1219],
    'NY':['New York',42.1497,-74.9384],
    'OH':['Ohio',40.3736,-82.7755],
    'OK':['Oklahoma',35.5376,-96.9247],
    'OR':['Oregon',44.5672,-122.1269],
    'PA':['Pennsylvania',40.5773,-77.2640],
    'PR':['Puerto Rico',18.2766,-66.3350],
    'RI':['Rhode Island',41.6772,-71.5101],
    'SC':['South Carolina',33.8191,-80.9066],
    'SD':['South Dakota',44.2853,-99.4632],
    'TN':['Tennessee',35.7449,-86.7489],
    'TX':['Texas',31.1060,-97.6475],
    'UT':['Utah',40.1135,-111.8535],
    'VA':['Virginia',37.7680,-78.2057],
    'VI':['Virgin Islands',18.0001,-64.8199],
    'VT':['Vermont',44.0407,-72.7093],
    'WA':['Washington',47.3917,-121.5708],
    'WI':['Wisconsin',44.2563,-89.6385],
    'WV':['West Virginia',38.4680,-80.9696],
    'WY':['Wyoming',42.7475,-107.2085],
    }
    return states

if __name__ == '__main__':
    main()