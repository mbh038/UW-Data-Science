import MapReduce
import sys

"""
Join in the Simple Python MapReduce Framework
"""  
mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[1]
    value =list(record)
    mr.emit_intermediate(key, value)    

def reducer(key, value):
    # key: word
    # value: list of occurrence count
    #print value
    for index in range(1,len(value)):
        mr.emit(value[0]+value[index])

# Do not modify below this line
# =============================
if __name__ == '__main__':
  #inputdata = open(sys.argv[1])
  inputdata = open("./data/records.json")

  mr.execute(inputdata, mapper, reducer)
