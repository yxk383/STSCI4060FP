file = open('D://E-Angel//Documents//STSCI4060FP//honeybee_gene_sequences.txt', 'r')
#print(file.readline()[-5:])

rawData = ''
processData = ''
finalData = []

for line in file:
    #print(line)
    rawData += line
    if(line[:3] == '>gi'):
        rawData += '_**gene_seq_starts_here**_'
    
print(rawData.find('58585251'))
#print(rawData)

# Remove all line switch signs
processData = rawData.replace('\n', '')

#print(processData)

# Split by > to form a list
'''
NOTE: By Python split() definition, if there is a delimiter in the beginning/end of the string,
the split() function will create empty string(s) at the beginning/end of result list, respectively.
In our case, there is a delimiter in the beginning of the string.
Therefore, pop the first element (an empty string) out.
'''
processData = processData.split('>')
processData.pop(0)

#print(processData[483])

dataLength = []
for data in processData:
    '''
    Split the data of each list so that only gene sequence remains.
    '''
    dataLength.append(len(data.split('_**gene_seq_starts_here**_')[1]))
    
#print(finalData[-1])


print(max(dataLength))

'''
According to the print result, the maximum length of all datasets is 14440
For convinence purpose, the length of the inputsize is set as 15000.
'''