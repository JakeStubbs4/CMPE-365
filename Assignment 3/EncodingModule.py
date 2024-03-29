# Jake Stubbs
# 20005204
# I certify that this submission contains my own work, except as noted.

def textFileToEncodingDictionary(codewords_file):
    line_list = codewords_file.readlines()
    codeword_dictionary = {}
    for line in line_list:
        # Split each line by the ': ' delimiter to a ascii code and a binary string.
        current_data = line.split(" ")
        ascii_code = current_data[0]
        # Remove additional line ending from codeword.
        codeword = current_data[1][0:len(current_data[1]) - 1]
        codeword_dictionary[ascii_code] = codeword
    return codeword_dictionary

def encodeFile(codeword_dictionary, plaintext_filename, codewords_filename):
    plaintext_file = open(plaintext_filename, "r+")
    encoded_filename = str(plaintext_filename[0:len(plaintext_filename) - 4]) + " " + str(codewords_filename[0:len(codewords_filename) - 4]) + " Encoded.txt"
    encoded_file = open(encoded_filename, "w+")
    file_contents = plaintext_file.read()
    for char in file_contents:
        if ord(char) == 10 or (ord(char) >= 32 and ord(char) <= 126):
            encoded_file.write(codeword_dictionary[str(ord(char))])
    return encoded_filename

def main():
    # Request a canonical collection to use for the alphabet frequencies
    canonical_collection = input("Enter the name of the canonical collection of which the alphabet frequencies were extracted, including the .zip file type: ")
    # Open the corresponding codeword file.
    codewords_filename = str(canonical_collection[0:len(canonical_collection) - 4]) + " Codewords.txt"
    codewords_file = open(codewords_filename, "r")
    codeword_dictionary = textFileToEncodingDictionary(codewords_file)
    # Encode a file using the dictionary defined in the codeword file
    plaintext_filename = input("Enter the name of the plaintext file to be encoded, including the .txt file extension: ")
    encoded_filename = encodeFile(codeword_dictionary, plaintext_filename, codewords_filename)
    print("The encoded file is now available in your directory named as follows: " + str(encoded_filename))

main()