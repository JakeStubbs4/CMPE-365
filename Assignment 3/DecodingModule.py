# Jake Stubbs
# 20005204
# I certify that this submission contains my own work, except as noted.

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
    for line in line_list:
        data_array.append(line.split(" "))

    root_node = decodingNode(None, None, None)
    for element in data_array:
        current_node = root_node
        element[1] = list(element[1])
        while(len(element[1]) > 0):
            current_bit = element[1].pop(0)
            if current_bit == '0':
                if current_node.left_child:
                    current_node = current_node.left_child
                else:
                    current_node.left_child = decodingNode(None, None, None)
                    current_node = current_node.left_child
            elif current_bit == '1':
                if current_node.right_child:
                    current_node = current_node.right_child
                else:
                    current_node.right_child = decodingNode(None, None, None)
                    current_node = current_node.right_child
            else:
                print("BROKEN: " + str(current_bit))
        current_node.character = chr(int(element[0]))
    return root_node

#def decodeFile(codeword_tree, encoded_filename):


def main():
    # Request a canonical collection to use for the alphabet frequencies
    canonical_collection = input("Enter the name of the canonical collection of which the alphabet frequencies were extracted, including the .zip file type: ")
    # Open the corresponding codeword file and construct a dictionary for decoding.
    codewords_filename = str(canonical_collection[0:len(canonical_collection) - 4]) + " Codewords.txt"
    codewords_file = open(codewords_filename, "r")
    codeword_tree = textFileToDecodingTree(codewords_file)
    print("Root Node: " + str(codeword_tree))
    print("Left Child: " + str(codeword_tree.left_child))
    print("Right Child: " + str(codeword_tree.right_child))
    # Encode a file using the dictionary defined in the codeword file
    # encoded_filename = input("Enter the name of the plaintext file to be encoded, including the .txt file extension: ")
    # decodeFile(codeword_tree, encoded_filename)

main()