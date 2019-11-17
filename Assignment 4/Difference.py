# Jake Stubbs
# 20005204
# Assignment 4: Get Difference

def stringCompare(string_1, string_2, strings_dictionary1, strings_dictionary2):
    if (strings_dictionary1[string_1] == strings_dictionary1[string_2]) and (strings_dictionary2[string_1] == strings_dictionary2[string_2]):
        if string_1 == string_2:
            return True
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
            strings_dictionary1[line] = hashString(line, 7, 100000)
            strings_dictionary2[line] = hashString(line, 6, 100000)
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

def main():
    filenames = str(input("Enter the filenames you wish to compare including their filetype seperated by a pipe (ie. file1.txt|file2.txt):"))
    files_list = filenames.split("|")
    strings_dictionary1, strings_dictionary2, files_lines = readFilesToDictionary(files_list)
    Table = LCSLTable(files_lines, strings_dictionary1, strings_dictionary2)
    matching_lines = recoverSequence(Table, files_lines, strings_dictionary1, strings_dictionary2)
    for pair in matching_lines:
        print(pair)

main()