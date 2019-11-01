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

# binaryInsert() inserts a node into the correct position of a sorted list based on the elements frequency.
def binaryInsert(sorted_nodes_list, element):
    # If the length of the list is <= 1 we can insert the element based on direct comparrison.
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
    # Otherwise we recurse on the appropriate half of the sorted list until it is of length <= 1:
    else:
        # Approximate the mid index of the sorted list, cannot be exact if the list is of odd length and subtract 1 for appropriate indexing.
        mid_index = math.floor(len(sorted_nodes_list)/2) - 1
        # If the node at the middle index has a greater frequency than the element to be inserted, then only the greater half of the entire list needs to be checked:
        if sorted_nodes_list[mid_index].frequency > element.frequency:
            # Append the greater half of the sorted list to the list resulting from the recursive call
            sorted_nodes_list = binaryInsert(sorted_nodes_list[0:mid_index], element) + sorted_nodes_list[mid_index:len(sorted_nodes_list)]
            return sorted_nodes_list
        # If the node at the middle index has a lesser frequency than the element to be inserted, then only the lesser half of the entire list needs to be checked:
        elif sorted_nodes_list[mid_index].frequency < element.frequency:
            # Append the result of the recursive call to the lesser half of the sorted list.
            sorted_nodes_list = sorted_nodes_list[0:mid_index+1] + binaryInsert(sorted_nodes_list[mid_index+1:len(sorted_nodes_list)], element)
            return sorted_nodes_list
        else:
            # If the middle node has the same frequency as the element to be inserted we can insert it directly adjacent to the middle element:
            sorted_nodes_list.insert(mid_index, element)
            return sorted_nodes_list

# readZipFile() takes a canonical collection and returns a list of all of the files contents.
# This function was adapted from https://codeyarns.com/2013/10/03/how-to-read-contents-of-zip-file-in-python/
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
        # Pop the two nodes with the lowest frequency values
        left_child = sorted_frequencies_nodes.pop(0)
        right_child = sorted_frequencies_nodes.pop(0)

        # Combine the nodes to create a new non-root node
        new_frequency = left_child.frequency + right_child.frequency
        new_ascii = [left_child.ascii_code, right_child.ascii_code]
        new_node = FrequencyNode([new_ascii, new_frequency], [left_child, right_child], max(left_child.depth + 1, right_child.depth + 1))

        # Insert the new node into the sorted list
        sorted_frequencies_nodes = binaryInsert(sorted_frequencies_nodes, new_node)

    return sorted_frequencies_nodes

# Writes codes to a text file named according to the canonical collection that was inputted by the user.
def writeCodesToFile(codeword_array, codeword_file):
    # Sort codeword array based on ascii code to have the desired structure of the text file.
    sorted_codewords = sorted(codeword_array, key=lambda kv: int(kv[0].ascii_code))
    for currentCode in sorted_codewords:
        currentCodeword = [val for val in currentCode[1] if val is not None]
        codeword_file.write(str(currentCode[0].ascii_code) + " " + str(''.join(currentCodeword)) + "\n")
    
# Takes the root node of a huffman tree and creates a text file containing the corresponding alphabets codewords.
def defineCodewords(huffman_root, currentCode, index, codewords):
    # If there is a left child, continue down the tree and write a 0 to the codeword.
    if (huffman_root.left_child):
        currentCode[index] = "0"
        defineCodewords(huffman_root.left_child, currentCode, index + 1, codewords)

    # If there is a right child, continue down the tree and write a 1 to the codeword.
    if (huffman_root.right_child):
        currentCode[index] = "1"
        defineCodewords(huffman_root.right_child, currentCode, index + 1, codewords)

    # If we have reached a root node, append the current code to a file based on the canonical collection in use.
    if (not huffman_root.left_child) and (not huffman_root.right_child):
        codewords.append([huffman_root, currentCode[0:index+1]])
    
    return codewords

def main():
    canonical_collection = input("Enter the name of the canonical collection in the form of a zip file from which to extract the alphabet frequencies, including the file type: ")
    line_list = readZipFile(canonical_collection)
    alphabet_frequencies = extractAlphabetFrequencies(line_list)
    huffman_root = createHuffmanTree(alphabet_frequencies)
    # Initialize arrays to be used in defineCodwords()
    codeword_array = [None for i in range(huffman_root[0].depth)]
    codewords = []
    codewords_results = defineCodewords(huffman_root[0], codeword_array, 0, codewords)
    # Initialize file based on inputted canonical_collection
    codeword_file = open(str(canonical_collection[0:len(canonical_collection) - 4]) + " Codewords.txt", "w+")
    writeCodesToFile(codewords_results, codeword_file)

main()