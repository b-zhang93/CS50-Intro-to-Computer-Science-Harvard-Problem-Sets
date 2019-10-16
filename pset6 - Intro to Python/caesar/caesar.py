from cs50 import get_string
from cs50 import get_int
from sys import argv


# check for CLA to be in order and return error message if so
if len(argv) != 2:
    print("Usage: ./caesar key k")
    exit(1)
# checks for integer and positive
elif not argv[1].isdigit():
    print("Usage: ./caesar key k")
    exit(1)

# defining the key and converting it to an integer
key = argv[1]
k = int(key)

# prompt for user and return cipher
word = get_string("plaintext: ")
print("ciphertext: ", end="")

# c is the iterator for each letter in input
for c in word:
    # for lowercase letters to convert and mod to wrap around then convert back to letter
    if c.islower():
        x = (ord(c) - 97 + k) % 26
        y = 97 + x
        z = chr(y)
        print(z, end="")
    # do the same for upper case
    elif c.isupper():
        x = (ord(c) - 65 + k) % 26
        y = 65 + x
        z = chr(y)
        print(z, end="")
    # every other non-alpha char just print it out no conversion
    else:
        print(c, end="")
print()
