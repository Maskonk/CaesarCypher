# Caesar cypher Encrypter/Decrypter
# Author: Kyle Walker
""" Using the Caesar Cypher encrypts or decrypts a string the user enters."""

# Import modules
from re import sub
from operator import itemgetter

# Set global variables
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
length = len(chars)
new = ""
matches = []
found = False
key2 = 0
not_found = False
wordlist = []


def encrypt_decrypt(string, mode, key):
    """Encrypts or decrypts a string string based on what mode is taken as a parameter for number of places key."""
    global chars
    global new
    # Remove all instances of space in the string with nothing
    string = sub(" ", "", string)
    string = string.upper()
    # For every character in the string loop
    for char in string:
        # Find the position of the character in the string
        index = chars.find(char)
        # If the mode encrypt is selected
        if mode == "encrypt":
            # If the position is greater than 25
            if index + key > (length - 1):
                # Start from the beginning of the string
                index -= length
            # Append the new character to the new string
            new += chars[index + key]
        # If the mode decrypt is selected
        elif mode == "decrypt":
            # If the posistion is less than 0
            if index - key < 0:
                # Start from the end of the string
                index += length
            # Append the new character to the new string
            new += chars[index - key]
        else:
            print("ERROR!")
            exit()


def crack(string):
    """Cracks a given string string by trying each of the twenty-five possible combinations then checking that for
    english words."""
    global chars
    global new
    global matches
    global not_found
    global wordlist
    # For every possible key
    try:
        # Open the dictionary file dict.txt
        with open("dict.txt", "r") as file:
            # Read the file
            lines = file.read()
            # Spilt the file into a list for every new line
            wordlist = lines.split("\n")
    except Exception as e:
        print("Error dictionary file not found. Please contact an Administrator.")
        exit(1)

    for x in range(1, length):
        new = ""
        # Call the work function with the string s and the key determined by the loop position
        encrypt_decrypt(string, "decrypt", x)
        # Call the find_words function to count the words in the cracked string for the key
        find_words(new)

    # If at least one word has been found in a string
    if found:
        # Sort dic by the number of matches
        matches = sorted(matches, key=itemgetter(0), reverse=True)
        # Print the most likely result which will be the first entry after sorting
        print("\nThe most likely result is:", matches[0][1], "with", str(matches[0][0]), "words identified. With a key of",
              str(matches[0][2]) + ".")
        print("Other possible likely results are: ")
        for x in range(1, len(matches)):
            if matches[x][0] != 0:
                # Print any other strings with matching results
                print("\n" + matches[x][1], "with", str(matches[x][0]), "words identified. With a key of", str(matches[x][2]) + ".")
            else:
                # Determine the end of the matching strings
                not_found = True
    # If no matches were made print all strings for the user to interpret
    else:
        print("No words were found in any of the strings. User interpretation required identified.")
        for x in range(0, len(matches)):
            print(matches[x][1])

    # Print none to signify the end of the matching strings
    if not_found is True:
        print("None.")


def menu():
    """Display a menu for the user, then runs a function based on the input from the user."""
    global new
    print("\nWelcome to the Caesar code encrypter/decypter")
    while True:
        print("\nPlease select an option:\n1. Encrypt a phrase.\n2. Decrypt a phrase.\n3. Crack a cypher.\n4. Exit. ")
        o = input("\nPlease enter a number to continue: ")
        if str(o) == "1":
            i = input("\nDo you want to: \n 1. Enter a string. \n 2. Use the test case. \n 3. Exit. \n "
                      "Please enter a number to continue: ")
            if str(i) == "1":
                i2 = get_input("Please enter a string to be encrypted: ")
                encrypt_decrypt(i2, "encrypt", 2)
                print("Your encrypted string is:", new)
                break
            elif str(i) == "2":
                encrypt_decrypt("Hello Suzanne", "encrypt", 2)
                print("Your encrypted string is:", new)
                break
            elif str(i) == "3":
                exit(0)
            else:
                print("That is not a valid input.")
                continue
        elif str(o) == "2":
            i = input("Do you want to: \n 1. Enter a string. \n 2. Use the test case. \n 3. Exit. \n "
                      "Please enter a number to continue: ")
            if str(i) == "1":
                i2 = get_input("Please enter a string to be decrypted: ")
                encrypt_decrypt(i2, "decrypt", 2)
                print("Your decrypted string is:", new)
                break
            elif str(i) == "2":
                encrypt_decrypt("IQQfOQtpKpIGXGtaQPG", "decrypt", 2)
                print("Your decrypted string is:", new)
                break
            elif str(i) == "3":
                exit(0)
            else:
                print("That is not a valid input.")
                continue
        elif str(o) == "3":
            i = input("Do you want to: \n 1. Enter a string. \n 2. Use the test case. \n 3. Exit. \n "
                      "Please enter a number to continue: ")
            if str(i) == "1":
                i2 = get_input("Please enter a string to be cracked: ")
                crack(i2)
                break
            elif str(i) == "2":
                crack("PBATENGHYNGVBAFLBHUNIRPENPXRQGURPBQRNAQGURFUVSGJNFGUVEGRRA")
                break
            elif str(i) == "3":
                exit(0)
            else:
                print("That is not a valid input.")
                continue
        elif str(o) == "4":
            exit(0)
        else:
            print("That is not a valid input.")
            continue


def find_words(comb):
    """Compares each word in the dictionary file dict.txt to the string comb to count how many words
    from the file are in the string. The number of words found are then appended to a list inside the list l.
    Only matches words with two or more characters to reduce variance."""
    global matches
    global found
    global key2
    global wordlist
    # Set count to zero
    count = 0
    key2 += 1
    # For every word in that list
    for word in wordlist:
        # If the word is in the string and the length of the matching word is longer than 2 characters
        if word in comb.lower() and len(word) > 2:
            # Add one to count
            count += 1

    # Append the number of matching words and the string to a list in l
    matches.append([count, comb, key2])
    # If count is greater than zero
    if count > 0:
        # Set found to true
        found = True


def get_input(s):
    """Get a string from the user. Take parameter s as the prompt for input. Then validates the input, if the
    input is not valid it asks the user for another input until a valid input is entered"""
    global chars
    a = False
    # Ask the user for an input, prompt gotten from paramter s
    i = input(s)
    # Convert the string to uppercase
    i = i.upper()
    # Loop until a valid string has been entered
    while a is False:
        # For every character in the string
        for ch in i:
            # If the character is not in the valid character set list
            if ch not in chars:
                # Print an error to the user
                print("That is not a valid input.")
                # Ask for a new input
                i = input(s)
            else:
                # When the user has entered a valid string end the loop
                a = True
    # Return the input
    return i


def main():
    menu()


if __name__ == "__main__":
    main()
