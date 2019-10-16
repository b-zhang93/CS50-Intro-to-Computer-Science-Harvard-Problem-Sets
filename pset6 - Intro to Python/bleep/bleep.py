from cs50 import get_string
from sys import argv


def main():
    # argument checks
    if len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)
    if argv[1].isdigit():
        print("Usage: python bleep.py dictionary")
        exit(1)

    # open the dictionary containing banned words that should be censored
    infile = argv[1]
    file = open(infile)
    words = set()

    # adds stripped words into the previously defined set called words
    for line in file:
        words.add(line.strip("\n"))
    file.close()

    # prompt for user input
    msg = get_string("What message would you like to censor? \n")

    # splits the string into an array of words
    word = msg.split()
    n = len(word)

    # iterate over each word
    for i in range(n):
        # if word is banned then print * for each letter
        if word[i].lower() in words:
            x = len(word[i])
            print("*" * x, end="")
            print("", end=" ")
        # if word is not banned, just print the word
        else:
            print(word[i], end=" ")
    print()


# to call main
if __name__ == "__main__":
    main()
