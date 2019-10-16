from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    # creating lists for a and b while separating by new lines
    seta = a.split("\n")
    setb = b.split("\n")
    identical = set()

    # iterates each item in a and checks if its in b, and if so adds to our set called identical
    for i in range(len(seta)):
        if seta[i] in setb:
            identical.add(seta[i])

    return identical


def sentences(a, b):
    """Return sentences in both a and b"""

    # uses tokenize to separate input by sentences and puts into a list
    seta = sent_tokenize(a)
    setb = sent_tokenize(b)
    identical = set()

    # iteration same as before
    for i in range(len(seta)):
        if seta[i] in setb:
            identical.add(seta[i])

    return identical


# creating a helper function to return list of substrings for substrings function
def substringof(n, x):

    subx = []
    # iterate through each character but as a block of i to n
    for i in range(len(x) - n + 1):
        sub = x[i:i + n]
        subx.append(sub)

    return subx


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # uses the helper function we created earlier to make list of substrings with n size
    seta = substringof(n, a)
    setb = substringof(n, b)
    identical = set()

    for i in range(len(seta)):
        if seta[i] in setb:
            identical.add(seta[i])

    return identical