import MapReduce
import sys

"""
Unique trims Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1][0:-10]
    mr.emit_intermediate(value, key)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    #print key
    
    mr.emit((key))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  #inputdata = open("./data/dna.json")
  mr.execute(inputdata, mapper, reducer)
