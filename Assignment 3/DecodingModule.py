# Jake Stubbs
# 20005204
# I certify that this submission contains my own work, except as noted.

import copy

class decodingNode:
    left_child = None
    right_child = None
    character = None

    def __init__(self, left_child, right_child, character):
        self.left_child = left_child
        self.right_child = right_child
        self.character = character

def textFileToDecodingTree(codewords_file):
    line_list = codewords_file.readlines()
    data_array = []
    # Create an array of ascii characters and their associated codeword by splitting at the space of each line.
    for line in line_list:
        data_array.append(line.split(" "))

    # Initialize the root node of our decoding tree.
    root_node = decodingNode(None, None, None)
    for element in data_array:
        # return to the root of the tree for each element.
        current_node = root_node
        # String to list to allow for use of .pop()
        element[1] = list(element[1])
        while(len(element[1]) > 1):
            # pop the 0th character from the current element and assign it to the current bit.
            current_bit = element[1].pop(0)
            if current_bit == '0':
                # Either traverse down the left branch or create it if it does not yet exist.
                if current_node.left_child:
                    current_node = current_node.left_child
                else:
                    current_node.left_child = decodingNode(None, None, None)
                    current_node = current_node.left_child
            elif current_bit == '1':
                # Either traverse down the right branch or create it if it does not yet exist.
                if current_node.right_child:
                    current_node = current_node.right_child
                else:
                    current_node.right_child = decodingNode(None, None, None)
                    current_node = current_node.right_child
            else:
                print("BROKEN: " + str(current_bit))
        # Once the codeword has no characters left (and our traversal is done) assign a character to the leaf node we have created.
        current_node.character = chr(int(element[0]))
    # Return the root node of the tree.
    return root_node

def decodeFile(codeword_tree, encoded_filename):
    encoded_file = open(encoded_filename, "r+")
    file_contents = encoded_file.read()
    plaintext_filename = str(encoded_filename[0:len(encoded_filename) - 11]) + "Decoded.txt"
    plaintext_file = open(plaintext_filename, "w+")
    current_node = copy.deepcopy(codeword_tree)

    # Greedy approach to decoding: As soon as you find a character, print it.
    for char in file_contents:
        if char == '0':
            # If the current node contains a character, print that character and return to the root of the tree.
            if current_node.left_child.character:
                plaintext_file.write(current_node.left_child.character)
                current_node = codeword_tree
            else:
                # If there is no character, step down the left branch of the tree.
                current_node = current_node.left_child
        elif char == '1':
            # If the current node contains a character, print that character and return to the root of the tree.
            if current_node.right_child.character:
                plaintext_file.write(current_node.right_child.character)
                current_node = codeword_tree
            else:
                # If there is no character, step down the right branch of the tree.
                current_node = current_node.right_child
        else:
            # If it is not a 0 or a 1 there is an issue (should not get here)
            print("BROKEN: " + str(current_node))
    return plaintext_filename

def main():
    # Request a canonical collection to use for the alphabet frequencies
    canonical_collection = input("Enter the name of the canonical collection of which the alphabet frequencies were extracted, including the .zip file type: ")
    # Open the corresponding codeword file and construct a dictionary for decoding.
    codewords_filename = str(canonical_collection[0:len(canonical_collection) - 4]) + " Codewords.txt"
    codewords_file = open(codewords_filename, "r")
    codeword_tree = textFileToDecodingTree(codewords_file)
    
    # Get name of original file that was encoded and then decode the file.
    encoded_filename = input("Enter the name of the plaintext file that was encoded which you now wish to decode, including the .txt file extension: ")
    encoded_filename = str(encoded_filename[0:len(encoded_filename) - 4]) + " " + str(codewords_filename[0:len(codewords_filename) - 4]) + " Encoded.txt"
    plaintext_filename = decodeFile(codeword_tree, encoded_filename)
    print("The decoded file is now available in your directory named as follows: " + str(plaintext_filename))

main()