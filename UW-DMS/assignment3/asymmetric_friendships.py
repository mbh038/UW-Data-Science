import MapReduce
import sys

"""
Asymmetric Friend Count in the Simple Python MapReduce Framework
"""  
# Part 1
mr = MapReduce.MapReduce()

# Part 2

#af=[()]
def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]

    mr.emit_intermediate((key,value),(value,key))
    mr.emit_intermediate((value,key),(key,value))

# Part 3
def reducer(AB, BA):
    if len(BA) ==1:
        mr.emit((AB[0],AB[1]))
   
# Part 4
inputdata = open(sys.argv[1])
#inputdata = open("./data/friends.json")
mr.execute(inputdata, mapper, reducer)