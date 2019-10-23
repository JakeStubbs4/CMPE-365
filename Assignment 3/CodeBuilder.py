# Jake Stubbs
# 20005204
# I certify that this submission contains my own work, except as noted.

import zipfile
import operator
import collections
import math

class FrequencyNode:
    ascii_code = None
    frequency = 0
    left_child = None
    right_child = None

    def __init__(self, parameters, children):
        self.ascii_code = parameters[0]
        self.frequency = parameters[1]
        self.left_child = children[0]
        self.right_child = children[1]

# binaryInsert() inserts a node into the minheap structure based on the elements frequency in O(logn) time.
def binaryInsert(sorted_nodes_list, element):
    if len(sorted_nodes_list) < 2:
        if sorted_nodes_list[0].frequency >= element.frequency:
            new_list = sorted_nodes_list.insert(0, element)
            return new_list
        else:
            new_list = sorted_nodes_list.append(element)
            return new_list
    else:
        mid_index = math.floor(len(sorted_nodes_list)/2) - 1
        if sorted_nodes_list[mid_index].frequency > element.frequency:
            return binaryInsert(sorted_nodes_list[ :mid_index], element)
        elif sorted_nodes_list[mid_index].frequency < element.frequency:
            return binaryInsert(sorted_nodes_list[mid_index: ], element)
        else:
            new_list = sorted_nodes_list.insert(mid_index, element)
            return new_list

# readZipFile() takes a canonical collection and returns a list of all of the files contents.
# This function was adapted from https://codeyarns.com/2013/10/03/how-to-read-contents-of-zip-file-in-python/ (NOT ENTIRELY MY OWN WORK)
def readZipFile(filepath):
    zfile = zipfile.ZipFile(filepath)
    line_list = []
    for finfo in zfile.infolist():
        ifile = zfile.open(finfo)
        line_list.append(ifile.readlines())
    return line_list

# extractAlphabetFrequencies() takes a list of all of the files contents and returns a dictionary containing the frequency of each character.
def extractAlphabetFrequencies(line_list):
    # Initialize the frequencies dictionary to 0 for all printable characters.
    frequencies_dictionary = {'10': 0}
    for i in range(32, 127):
        frequencies_dictionary[str(i)] = 0
    
    # Traverse through each character in each file and increase the frequencies of the printable characters.
    for line in line_list:
        for element in line:
            for char in element:
                if (char == 10) or (char <= 126 and char >= 32):
                    # Increment frequency corresponding to printable character.
                    frequencies_dictionary[str(char)] = frequencies_dictionary[str(char)] + 1
    return frequencies_dictionary

# defineCodewords() takes a dictionary of alphabet frequencies and creates a text file containing the generated codewords.
def defineCodewords(alphabet_frequencies):
    # Sort the alphabet frequencies by order of increasing frequency.
    sorted_frequencies = sorted(alphabet_frequencies.items(), key=lambda kv: kv[1])
    sorted_frequencies_nodes = []
    for frequency in sorted_frequencies:
        sorted_frequencies_nodes.append(FrequencyNode(frequency, [None, None]))

    new_list = []
    for i in range(5):
        if i != 3:
            new_list.append(FrequencyNode([None, i], [None, None]))
    
    for elem in new_list:
        print(elem.frequency)

    element = FrequencyNode([None, 3], [None, None])
    new_list = binaryInsert(new_list, element)

    for elem in new_list:
        print(elem.frequency)

    # Create a Huffman tree containing all of the frequency nodes.
    while(len(sorted_frequencies_nodes) > 1):
        left_child = sorted_frequencies_nodes.pop(0)
        right_child = sorted_frequencies_nodes.pop(0)
        frequency = left_child.frequency + right_child.frequency
        new_node = FrequencyNode([None, frequency], [left_child, right_child])
        sorted_frequencies_nodes = binaryInsert(sorted_frequencies_nodes, new_node)
        for freq in sorted_frequencies_nodes:
            print(freq.frequency)
            print(freq.ascii_code)

    # Initialize the codewords dictionary to "" for all printable characters.
    alphabet_codewords = {'10': ""}
    for i in range(32, 127):
        alphabet_codewords[str(i)] = ""

    return alphabet_codewords

def main():
    canonical_collection = input("Enter the name of the canonical collection from which to extract the frequencies, including the file type: ")
    line_list = readZipFile(canonical_collection)
    alphabet_frequencies = extractAlphabetFrequencies(line_list)
    alphabet_codewords = defineCodewords(alphabet_frequencies)
    print(alphabet_codewords)

main()