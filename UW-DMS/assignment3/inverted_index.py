dimport MapReduce
import sys

"""
Inverted Index in the Simple Python MapReduce Framework
"""
#record = open(sys.argv[1])
# record = open("./data/books.json")
    
mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    #print key
    value = record[1]
    words = value.split()
    for w in words:
      mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    docList=[]
    for v in list_of_values:
      if v not in docList:
          docList.append(v)
    mr.emit((key, docList))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  #inputdata = open(sys.argv[1])
  inputdata = open("./data/books.json")


  mr.execute(inputdata, mapper, reducer)
