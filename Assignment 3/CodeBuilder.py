# Jake Stubbs
# 20005204
# I certify that this submission contains my own work, except as noted.

import zipfile
import operator
import collections
import math
import copy

class FrequencyNode:
    ascii_code = None
    frequency = 0
    left_child = None
    right_child = None
    depth = 0

    def __init__(self, parameters, children, depth):
        self.ascii_code = parameters[0]
        self.frequency = parameters[1]
        self.left_child = children[0]
        self.right_child = children[1]
        self.depth = depth

# binaryInsert() inserts a node into the minheap structure based on the elements frequency in O(logn) time.
def binaryInsert(sorted_nodes_list, element):
    if len(sorted_nodes_list) <= 1:
        if len(sorted_nodes_list) == 0:
            sorted_nodes_list.append(element)
            return sorted_nodes_list
        elif sorted_nodes_list[0].frequency >= element.frequency:
            sorted_nodes_list.insert(0, element)
            return sorted_nodes_list
        else:
            sorted_nodes_list.append(element)
            return sorted_nodes_list
    else:
        mid_index = math.floor(len(sorted_nodes_list)/2) - 1
        if sorted_nodes_list[mid_index].frequency > element.frequency:
            sorted_nodes_list = binaryInsert(sorted_nodes_list[0:mid_index], element) + sorted_nodes_list[mid_index:len(sorted_nodes_list)]
            return sorted_nodes_list
        elif sorted_nodes_list[mid_index].frequency < element.frequency:
            sorted_nodes_list = sorted_nodes_list[0:mid_index+1] + binaryInsert(sorted_nodes_list[mid_index+1:len(sorted_nodes_list)], element)
            return sorted_nodes_list
        else:
            sorted_nodes_list.insert(mid_index, element)
            return sorted_nodes_list

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

# createHuffmanTree() takes a dictionary of alphabet frequencies and returns the root node of the corresponding huffman tree.
def createHuffmanTree(alphabet_frequencies):
    # Sort the alphabet frequencies by order of increasing frequency.
    sorted_frequencies = sorted(alphabet_frequencies.items(), key=lambda kv: kv[1])
    sorted_frequencies_nodes = []
    for frequency in sorted_frequencies:
        sorted_frequencies_nodes.append(FrequencyNode(frequency, [None, None], 0))

    # Create a Huffman tree containing all of the frequency nodes.
    while(len(sorted_frequencies_nodes) >= 2):
        left_child = sorted_frequencies_nodes.pop(0)
        right_child = sorted_frequencies_nodes.pop(0)
        new_frequency = left_child.frequency + right_child.frequency
        new_ascii = [left_child.ascii_code, right_child.ascii_code]
        new_node = FrequencyNode([new_ascii, new_frequency], [left_child, right_child], max(left_child.depth + 1, right_child.depth + 1))
        sorted_frequencies_nodes = binaryInsert(sorted_frequencies_nodes, new_node)
    #print("Root Node Ascii:" + str(sorted_frequencies_nodes[0].ascii_code) + ". Frequency: " + str(sorted_frequencies_nodes[0].frequency))
    #print("Root Left Child Ascii: " + str(sorted_frequencies_nodes[0].left_child.ascii_code) + ". Frequency: " + str(sorted_frequencies_nodes[0].left_child.frequency))
    #print("Root Right Child Ascii: " + str(sorted_frequencies_nodes[0].right_child.ascii_code) + ". Frequency: " + str(sorted_frequencies_nodes[0].right_child.frequency))

    return sorted_frequencies_nodes

# Writes codes to a file named according to the canonical collection that was inputted by the user.
def appendCodeToFile(huffman_root, currentCode, index, canonical_collection):
    print(str(huffman_root.ascii_code) + ": " + str(currentCode[0:index+1]))

# Takes the root node of a huffman tree and creates a text file containing the corresponding alphabets codewords.
def defineCodewords(huffman_root, currentCode, index, canonical_collection):
    if (huffman_root.left_child):
        currentCode[index] = 0
        defineCodewords(huffman_root.left_child, currentCode, index + 1, canonical_collection)

    if (huffman_root.right_child):
        currentCode[index] = 1
        defineCodewords(huffman_root.right_child, currentCode, index + 1, canonical_collection)

    if (not huffman_root.left_child) and (not huffman_root.right_child):
        appendCodeToFile(huffman_root, currentCode, index, canonical_collection)

def main():
    canonical_collection = input("Enter the name of the canonical collection in the form of a zip file from which to extract the alphabet frequencies, including the file type: ")
    line_list = readZipFile(canonical_collection)
    alphabet_frequencies = extractAlphabetFrequencies(line_list)
    print(alphabet_frequencies)
    huffman_root = createHuffmanTree(alphabet_frequencies)
    codeword_array = [None for i in range(huffman_root[0].depth)]
    defineCodewords(huffman_root[0], codeword_array, 0, canonical_collection)

main()