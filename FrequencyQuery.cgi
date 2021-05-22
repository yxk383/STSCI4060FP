"""
STSCI 4060 Final Project
Yunxi Kou - yk799

The CGI file that accepts the input path,
processes the data file provided by HTML link,
and store the result into Oracle SQL database
"""
import cgi
import cx_Oracle

def main():
    contents = processInput()
    print(contents)

def processInput():
    '''
    
    '''
    con = cx_Oracle.connect("python/py39fp")
    cur = con.cursor()
    
    '''
    TODO:
    QUERY THE ENTIRE TABLE, FIND OUT THE HIGHEST RELATIVE FREQUENCIES OF A, C, G, T (NO GC HERE) BY A DICTIONARY OF FORMATTED STRINGS (see PPT 11 for detail)
    THEN, DESIGN AN OUTPUT DATATYPE (maybe)AS A LIST OF FORMATTED STRINGS TO STORE ALL POSSIBLE GI NUMBERS FOR THAT OCCURANCE.
    CORRESPONDING HTML TABLE WILL BE DESIGNED LATER.
    FILL IN THE MAKEPAGE() AFTER THAT
    '''
    aaList = ['A', 'C', 'G', 'T']
    fList = [() for t in range(4)]
    for i in range(len(aaList)):
        giNumbers = '' # If there are multiple genes with the same percentage, append their gi numbers all in this string.
        stringDict = {'aa': aaList[i]}
        obj = cur.execute('''
                          SELECT gi, freq_%(aa)s
                          FROM BeeGenes, (SELECT MAX(freq_%(aa)s) AS max%(aa)s FROM BeeGenes)
                          WHERE BeeGenes.freq_%(aa)s = max%(aa)s
                          ''' % stringDict) # NOTE: dictionary + format string
        
        for queryLine in obj:
            '''
            Under the same loop, one and only one element of A, C, G, T is chosen.
            Therefore, if multiple results are returned by query result obj within one loop,
            this indicates one nucleotide max value is shared by several genes.
            Use this loop to combine all their gi numbers, indiciated by queryLine[0], to one string, delimited by line switch sign.
            If there is only one result returned, this loop is equivalent to adding a line switch sign behind its gi number.
            '''
            giNumbers += (queryLine[0] + '\n') 
            combine_gi_tuple = (giNumbers, queryLine[1])
            fList[i] = combine_gi_tuple
            #print(queryLine)
            #fList[i] = queryLine # TODO: MODIFY THE DATA STRUCTURE HERE TO ENSURE MULTIPLE SAME RESULTS CAN BE STORED IN QUERY LIST.
            
    #print(fList)
            
    resultTuple = ()
    for j in range(4):
        resultTuple = resultTuple + fList[j]
        
    #print(resultTuple)
    
    cur.close()
    con.close()
    
    return makePage('resultTableTemplate.html', resultTuple) # TODO: PASS AN HTML TEMPLATE OF RESULT HERE. Use the table for makepage.

def fileToStr(fileName):
    templateFile = open(fileName)
    content = templateFile.read()
    templateFile.close()
    return content

def makePage(templateFileName, substitution):
    pageTemplate = fileToStr(templateFileName)
    return pageTemplate % substitution

try:
    print("Content-type: text/html\n\n")
    main()
except:
    cgi.print_exception()