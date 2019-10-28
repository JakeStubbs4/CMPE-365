# Jake Stubbs
# 20005204
# I certify that this submission contains my own work, except as noted.

def textFileToDecodingDictionary(codewords_file):
    

def main():
    # Request a canonical collection to use for the alphabet frequencies
    canonical_collection = input("Enter the name of the canonical collection of which the alphabet frequencies were extracted, including the .zip file type: ")
    # Open the corresponding codeword file and construct a dictionary for decoding.
    codewords_filename = str(canonical_collection[0:len(canonical_collection) - 4]) + " Codewords.txt"
    codewords_file = open(codewords_filename, "r")
    codeword_dictionary = textFileToDecodingDictionary(codewords_file)
    # Encode a file using the dictionary defined in the codeword file
    encoded_filename = input("Enter the name of the plaintext file to be encoded, including the .txt file extension: ")
    decodeFile(codeword_dictionary, encoded_filename)

main()