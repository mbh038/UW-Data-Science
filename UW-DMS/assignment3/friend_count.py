import MapReduce
import sys

"""
Friend Count in the Simple Python MapReduce Framework
"""  
mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key=record[0]
    value=record[1]
    mr.emit_intermediate(key, 1)
    
    
def reducer(key, value):
    # key: word
    # value: list of occurrence counts
    total = 0
    for v in value:
      total += v
    mr.emit((key, total))


# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  #inputdata = open("./data/friends.json")

  mr.execute(inputdata, mapper, reducer)
