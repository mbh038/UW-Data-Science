import MapReduce
import sys

"""
Join in the Simple Python MapReduce Framework
"""
#record = open(sys.argv[1])
#record = open("./data/records.json")
    
mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    recordID = record[1]
    #print recordID
    #print key
#    recordType = record[0]
#    for attribute in record:
    mr.emit_intermediate(key, value)
    #print mr.emit_intermediate(recordID, record[1])
    

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    joinRecords=[]
    #print list_of_values


    for v in list_of_values:
        #print key,v
        joinRecords.append(v)
    mr.emit((key, joinRecords))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  #inputdata = open(sys.argv[1])
  inputdata = open("./data/records.json")


  mr.execute(inputdata, mapper, reducer)
