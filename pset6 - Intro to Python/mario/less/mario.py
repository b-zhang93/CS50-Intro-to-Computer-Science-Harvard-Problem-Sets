from cs50 import get_string
from cs50 import get_int
from cs50 import get_char


# defining our get positive integer control function
def get_positive_int(prompt):
    while True:
        n = get_int(prompt)
        if n > 0 and n < 9:
            break
    return n


s = get_positive_int("Height: ")

for i in range(s):
    # defining our count variables for incrementing the print of hashes and spaces
    x = i + 1
    y = s - 1
    z = y - i
    # printing the hashes by the times of rows they are in, and vice versa for space - 1
    print(" " * z, end="")
    print("#" * x)