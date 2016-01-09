import MapReduce
import sys

"""
Matrix Multiplication in the Simple Python MapReduce Framework

"""
### Multiply.py 

# Part 1
mr = MapReduce.MapReduce()

# Part 2
def mapper(record):
    #print record
    matrixID=record[0]
    rowID=record[1]
    colID=record[2]
    value=record[3]

    mr.emit_intermediate(1,(matrixID,rowID,colID,value))
    #mr.emit_intermediate(colID,(matrixID,rowID,colID,value))
   # mr.emit_intermediate(rowID,value)

   # mr.emit_intermediate((colID,rowID),(matrixID,value))
    #mr.emit_intermediate((matrixID,colID), value)
   # mr.emit_intermediate((matrixID,rowID,colID), value)
        

# Part 3
def reducer(key, list_of_values):
#    print key
# 
#    product=0
#    for item in list_of_values:
#        print item
    
    aMatrix=[]
    for item in list_of_values:
        if item[0]=="a":
            aMatrix.append(item)
    bMatrix=[]
    for item in list_of_values:
        if item[0]=="b":
            bMatrix.append(item)
#    for item in aMatrix:
#        print item
#    print len(aMatrix)
#    print
#    for item in bMatrix:
#        print item        
#    print len(bMatrix)
#    print
    nRows = max(x[1] for x in aMatrix)+1
    nCols = max(x[2] for x in bMatrix)+1
#    print nRows,nCols 
    
     
    for i in range(nRows):        
        
        for j in range(nCols):
            product=0
            for k in range(nCols):
                #print i,j,product
                for l in range(len(aMatrix)):
                    for m in range(len(bMatrix)):
                    
                    
                        if aMatrix[l][1]==i and aMatrix[l][2]==k and bMatrix[m][1]==k and bMatrix[m][2]==j:
                            product += aMatrix[l][3]*bMatrix[m][3] 
            #print i,j,product
            mr.emit((i,j,product))
    
# Part 4

inputdata = open(sys.argv[1])
#inputdata = open("./data/matrix.json")

mr.execute(inputdata, mapper, reducer)