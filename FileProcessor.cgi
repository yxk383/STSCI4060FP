"""
STSCI 4060 Final Project
Yunxi Kou - yk799

The CGI file that accepts the input path,
processes the data file provided by HTML link,
and store the result into Oracle SQL database
"""
import time
import cgi
import cx_Oracle

def main():
    form = cgi.FieldStorage() # cgi script line
    filePath = form.getfirst('filePath') # Retrieve the file path from website user input.
    contents = processInput(filePath)
    print(contents)

def processInput(filepath):
    '''
    Process queries and frequency calculation.
    '''
    con = cx_Oracle.connect("python/py39fp")
    startTime = time.time()
    cur = con.cursor()
    cur.execute("DROP TABLE beeGenes") # UNCOMMENT THIS LINE IF TABLE ALREADY CREATED.
    cur.execute(
        """
        CREATE TABLE beeGenes (
            gi VARCHAR2(10),
            sequence CLOB,
            freq_A number,
            freq_C number,
            freq_G number,
            freq_T number,
            freq_GC number
        )
        """)
    # TODO: Follow the procedure on PPT to set an optimal bindarraysize when query is running.
    barraysize = 20
    cur.bindarraysize = barraysize #TEST VARIABLE, WILL BE CHANGED
    cur.setinputsizes(10, 15000, float, float, float, float, float) # See FildInputSize.py for setup detail.
    
    # Read raw data from a file
    infile = open(filepath, 'r')
    rawData = ''
    processData = ''
    
    # Form a string with the raw data
    # append _**gene_seq_starts_here**_ before the start of each sequence.
    for line in infile:
        #print(line)
        rawData += line
        if(line[:3] == '>gi'):
            rawData += '_**gene_seq_starts_here**_'
            
    # Form a continuous string.
    processData = rawData.replace('\n', '')
    
    # Change the string into a list, one gene sequence per list item.
    '''
    NOTE: By Python split() definition, if there is a delimiter in the beginning/end of the string,
    the split() function will create empty string(s) at the beginning/end of result list, respectively.
    In our case, there is a delimiter in the beginning of the string.
    Therefore, pop the first element (an empty string) out.
    '''
    processData = processData.split('>')
    processData.pop(0)
    
    for dataline in processData:
        '''
        Extract GI number, sequence and frequency from each element of list.
        '''
        # Find GI number
        gi_start = dataline.find('gi|') + 3 # length of |gi
        gi_end = dataline.find('|', gi_start)
        gi = dataline[gi_start: gi_end]
        # Find sequence
        seq_start = dataline.find('_**gene_seq_starts_here**_') + 26 # length of this string indicator
        seq = dataline[seq_start:]
        # Find frequency
        seqLength = len(seq)
        freq_A = seq.count('A') / float(seqLength)
        freq_C = seq.count('C') / float(seqLength)
        freq_G = seq.count('G') / float(seqLength)
        freq_T = seq.count('T') / float(seqLength)
        freq_GC = freq_C + freq_G
        
        # Execute query for each GI, sequence and frequency.
        cur.execute('''
                    INSERT INTO beeGenes
                    (gi, sequence, freq_A, freq_C, freq_G, freq_T, freq_GC)
                    values(:v1, :v2, :v3, :v4, :v5, :v6, :v7)
                    ''', (gi, seq, freq_A, freq_C, freq_G, freq_T, freq_GC))
        
    con.commit()
    stopTime = time.time()
    elapsed = stopTime - startTime
    print(f"The time elapsed using {barraysize} bindarraysize is : {elapsed} seconds\n")
    
    cur.close()
    con.close()
    
    return makePage('done_submission_template.html', ("Thank you for uploading."))

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