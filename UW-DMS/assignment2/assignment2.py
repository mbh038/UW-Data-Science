## -*- coding: utf-8 -*-
#"""
#Created on Sat Dec 26 06:43:01 2015
#
#@author: Mike
#"""
#
import sqlite3
import operator
conn = sqlite3.connect('reuters.db')
cur = conn.cursor()
#cur.execute('DROP TABLE IF EXISTS Frequency ')

## Problem 1
#
## Part a

cur.execute('''
SELECT count(*) FROM (
  SELECT * FROM Frequency WHERE docid="10398_txt_earn"
) x;
    ''')
ans_a=str(cur.fetchone()[0])
conn.commit()
print "part_a= ",ans_a
part_a=open("part_a.txt",'w')
part_a.write(ans_a)
part_a.close()

## Part b

cur.execute('''
SELECT count(*) FROM (
  SELECT Frequency.term FROM Frequency WHERE docid="10398_txt_earn" AND count=1
) x;
    ''')
ans_b=str(cur.fetchone()[0])
conn.commit()
print "part_b= ",ans_b
part_b=open("part_b.txt",'w')
part_b.write(ans_b)
part_b.close()

## Part c

cur.execute('''
SELECT count(*) FROM (
  SELECT Frequency.term FROM Frequency WHERE docid="10398_txt_earn" AND count=1
  UNION
  SELECT Frequency.term FROM Frequency WHERE docid="925_txt_trade" AND count=1
) x;
    ''')
ans_c=str(cur.fetchone()[0])
conn.commit()
print "part_c= ",ans_c
part_c=open("part_c.txt",'w')
part_c.write(ans_c)
part_c.close()

## Part d

cur.execute('''
SELECT count(*) FROM (
 SELECT DISTINCT Frequency.docid FROM Frequency
WHERE term Like '% legal %' 
OR term Like '% legal' 
OR term Like 'legal %' 
OR term = 'legal'
OR term Like '% law %' 
OR term Like '% law' 
OR term Like 'law %' 
OR term = 'law'
) x;
    ''')
ans_d=str(cur.fetchone()[0])
conn.commit()
print "part_d= ",ans_d
part_d=open("part_d.txt",'w')
part_d.write(ans_d)
part_d.close()

## Part e

cur.execute('''
SELECT count(*) FROM (
SELECT docid, COUNT(count) as Nterms FROM Frequency
GROUP BY docid
HAVING NTerms>300
) x;
    ''')
ans_e=str(cur.fetchone()[0])
conn.commit()
print "part_e= ",ans_e
part_e=open("part_e.txt",'w')
part_e.write(ans_e)
part_e.close()

## Part f

cur.execute('''
SELECT count(*) FROM (
SELECT docid
FROM Frequency
WHERE term IN ('transaction', 'world')
GROUP BY docid
HAVING COUNT(*) = 2
) x;
    ''')
ans_f=str(cur.fetchone()[0])
conn.commit()
print "part_f= ",ans_f
part_f=open("part_f.txt",'w')
part_f.write(ans_f)
part_f.close()

#end of Problem 1
cur.close()
# Problem 2

conn = sqlite3.connect('matrix.db')
cur = conn.cursor()

## part g

cur.execute('''
SELECT a.row_num,b.col_num,SUM(a.value*b.value) as product
FROM a,b
WHERE a.col_num=b.row_num
GROUP BY a.row_num,b.col_num
HAVING a.row_num=2 AND b.col_num=3
   ''')

ans_g=cur.fetchone()
conn.commit()
print "part_g= ", ans_g
ans_g=str(ans_g[2])
part_g=open("part_g.txt",'w')
part_g.write(ans_g)
part_g.close()

## Part h

#back to the Frequency db
cur.close()

# Problem 2

# part h

conn = sqlite3.connect('reuters.db')
cur = conn.cursor()

cur.execute('SELECT * FROM Frequency')
f=cur.fetchall()
doc1={}
for item in f:
    if item[0] =='10080_txt_crude':
        doc1[item[1]]=doc1.get(item[1],0)+item[2]

doc2={}
for item in f:
    if item[0] =='17035_txt_earn':
        doc2[item[1]]=doc2.get(item[1],0)+item[2]

similarity=0
for term in doc1:
    if term in doc2:
        similarity +=doc1[term]*doc2[term]

print "part_h= ", similarity
part_h=open("part_h.txt",'w')
part_h.write(str(similarity))
part_h.close()
cur.close()

## Part i

# open the connection#

import sqlite3
import operator
conn = sqlite3.connect('reuters.db')
cur = conn.cursor()

# add query terms to the corpus

#cur.executescript('''
#INSERT OR IGNORE INTO Frequency (docid,term,count) VALUES ('q','washington',1);
#INSERT OR IGNORE INTO Frequency (docid,term,count) VALUES ('q','taxes',1);
#INSERT OR IGNORE INTO Frequency (docid,term,count) VALUES ('q','treasury',1);
#''')

query=raw_input("Enter query: ")
print query
query=query.rstrip()
queryItems=query.split()
for item in queryItems:
    print item
    cur.execute('INSERT OR IGNORE INTO Frequency (docid,term,count) VALUES ("q",?,1)',(item,))
        
# return tuples of (docid, term, count) for whole dbase
cur.execute('SELECT * FROM Frequency')
f=cur.fetchall()
print len(f)
print f[0:10]
# construct dictionary of query terms
qdoc={}
for item in f:
    if item[0] =='q':
        qdoc[item[1]]=qdoc.get(item[1],0)+item[2]
print qdoc        
# construct list of unique terms
docList=[]
for triple in f:
    if triple[0] not in docList:
        docList.append(triple[0])
print len(docList)


similarity={}
count=0
for docid in docList:
    
    similarity[docid]=0
    docDict={}
    for item in f:
        if item[0] ==docid:
            docDict[item[1]]=docDict.get(item[1],0)+item[2]
    for term in docDict:
        if term in qdoc:
            similarity[docid] +=docDict[term]*qdoc[term]
    #print docid, similarity[docid]
    count +=1
mostSimilar= max(similarity.iteritems(), key=operator.itemgetter(1))

print "part_i= ", mostSimilar
part_i=open("part_i.txt",'w')
part_i.write(str(mostSimilar[1]))
part_i.close()

# remove query from database
conn = sqlite3.connect('reuters.db')
cur = conn.cursor()
cur.execute('''
DELETE FROM Frequency where docid='q';
''')
conn.commit()
cur.close()
    
    

