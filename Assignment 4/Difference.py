# Jake Stubbs
# 20005204
# Assignment 4: Get Difference
import collections

def stringCompare(string_1, string_2, strings_dictionary1, strings_dictionary2):
    if (strings_dictionary1[string_1] == strings_dictionary1[string_2]) and (strings_dictionary2[string_1] == strings_dictionary2[string_2]):
        if string_1 == string_2:
            return True
        else:
            print("Collision")
    else:
        return False

def hashString(string, a, b):
    result = 0
    for char in string:
        result = (a*result + ord(char)) % b
    return result

def readFilesToDictionary(files_list):
    strings_dictionary1 = {}
    strings_dictionary2 = {}
    files_lines = []
    i = 0
    for filename in files_list:
        files_lines.append([])
        file = open(filename, "r")
        for line in file.readlines():
            files_lines[i].append(line)
            strings_dictionary1[line] = hashString(line, 7, 2147483647)
            strings_dictionary2[line] = hashString(line, 11, 2147483647)
        i = i + 1
    return strings_dictionary1, strings_dictionary2, files_lines

def getData(i, j, Table, files_lines, strings_dictionary1, strings_dictionary2):
    if i == 0 and j == 0:
        if stringCompare(files_lines[0][0], files_lines[1][0], strings_dictionary1, strings_dictionary2) == True:
            return 1
        else:
            return 0
    if i == 0:
        if (stringCompare(files_lines[0][0], files_lines[1][j], strings_dictionary1, strings_dictionary2) == True) or (stringCompare(files_lines[0][0], files_lines[1][j-1], strings_dictionary1, strings_dictionary2) == True):
            return 1
        else:
            return 0
    if j == 0:
        if (stringCompare(files_lines[0][i], files_lines[1][0], strings_dictionary1, strings_dictionary2) == True) or (stringCompare(files_lines[0][i-1], files_lines[1][0], strings_dictionary1, strings_dictionary2) == True):
            return 1
        else:
            return 0
    if stringCompare(files_lines[0][i], files_lines[1][j], strings_dictionary1, strings_dictionary2) == True:
        return 1 + Table[i-1][j-1]
    else:
        return max(Table[i-1][j], Table[i][j-1], Table[i-1][j-1])

def LCSLTable(files_lines, strings_dictionary1, strings_dictionary2):
    Table = [[0 for j in range(len(files_lines[1]))] for i in range(len(files_lines[0]))]
    for i in range(len(files_lines[0])):
        for j in range(len(files_lines[1])):
            Table[i][j] = getData(i, j, Table, files_lines, strings_dictionary1, strings_dictionary2)
    return Table

def recoverSequence(Table, files_lines, strings_dictionary1, strings_dictionary2):
    matching_lines = []
    i = len(files_lines[0]) - 1
    j = len(files_lines[1]) - 1
    while((i is not -1) or (j is not -1)):
        if stringCompare(files_lines[0][i], files_lines[1][j], strings_dictionary1, strings_dictionary2) == True:
            matching_lines.insert(0, (i, j))
            i = i - 1
            j = j - 1
        else:
            maximum_predecessor = max(Table[i-1][j], Table[i][j-1], Table[i-1][j-1])
            if Table[i-1][j] == maximum_predecessor:
                i = i-1
            elif Table[i][j-1] == maximum_predecessor:
                j = j - 1
            else:
                i = i - 1
                j = j - 1
    return matching_lines

def displayOutput(matching_lines, files_list, file1_length, file2_length):
    m = 0
    output_dictionary = {}
    [p, q] = matching_lines[m]
    if(p != 0 or q!=0):
        Pval = [1, p+1] if p!=0 else ['None']
        Qval = [1, q+1] if q!=0 else ['None']
        output_dictionary[tuple(Pval+Qval)] = 'Mismatch'
    while(p < file1_length and q < file2_length and m < len(matching_lines)):
        pstart=p
        qstart=q
        pend=p
        qend=q
        while(m < len(matching_lines) and matching_lines[m] == (p, q)):
            pend=p
            qend=q
            p=p+1
            q=q+1
            m=m+1
        Pval = [pstart+1, pend+1]
        Qval = [qstart+1, qend+1]
        output_dictionary[tuple(Pval+Qval)] = 'Match'
        if(m>=len(matching_lines)):
            break
        [nextp,nextq] = matching_lines[m]
        Pval = [Pval[1]+1, nextp] if Pval[1]!=nextp else ['None']
        Qval = [Qval[1]+1, nextq] if Qval[1]!=nextq else ['None']
        output_dictionary[tuple(Pval+Qval)] = 'Mismatch'
        p=nextp
        q=nextq
    if(p!=file1_length or q!=file2_length):
        Pval = [p+1, file1_length] if p!=file1_length else ['None']
        Qval = [q+1, file2_length] if q!=file2_length else ['None']
        output_dictionary[tuple(Pval+Qval)] = 'Mismatch'
    for key in output_dictionary:
        vals = list(key)
        if (vals[0]=='None'):
            Pdisplay = 'None'
            Qdisplay = '<{} .. {}>'.format(vals[1],vals[2]) if vals[1]!='None' else 'None'
        else:
            Pdisplay = '<{} .. {}>'.format(vals[0],vals[1]) 
            Qdisplay = '<{} .. {}>'.format(vals[2],vals[3]) if vals[2]!='None' else 'None'
        print('{}: {}: {}  {}: {}\n'.format(output_dictionary[key], files_list[0], Pdisplay, 
            files_list[1], Qdisplay))

def main():
    filenames = str(input("Enter the filenames you wish to compare including the folder structure and filetype seperated by a pipe (ie. file1.txt|file2.txt):"))
    files_list = filenames.split("|")

    # Create two seperate dictionaries corresponding to the two hashing functions and return the lines of the files.
    strings_dictionary1, strings_dictionary2, files_lines = readFilesToDictionary(files_list)

    # Create the dynamic programming table given the files lines and the two dictionaries.
    Table = LCSLTable(files_lines, strings_dictionary1, strings_dictionary2)

    # Recover the longest common sequence of lines in the form of an array of tuples of line indices.
    matching_lines = recoverSequence(Table, files_lines, strings_dictionary1, strings_dictionary2)

    # Get Filenames without path structure:
    files_list[0] = files_list[0].split("/")[1]
    files_list[1] = files_list[1].split("/")[1]

    displayOutput(matching_lines, files_list, len(files_lines[0]), len(files_lines[1]))

if __name__=='__main__':
    main()
