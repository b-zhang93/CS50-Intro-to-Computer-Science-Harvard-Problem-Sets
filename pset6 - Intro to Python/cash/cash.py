from cs50 import get_float
from cs50 import get_int
from cs50 import get_string


# defining our function to get positive inputs only
def get_pos_float(prompt):
    while True:
        n = get_float(prompt) * 100
        if n > 0:
            break
    return n


# defining the coins as variables
qtr = 25
dm = 10
nic = 5
pen = 1

# get float and convert to int
c = get_pos_float("Change Owed: ")
cash = int(c)

# using modulo instead of while loops to calculate how many coins for change as per the challenge in the problem set
q = (cash // qtr)
d = ((cash % qtr) // dm)
n = ((cash % qtr) % dm) // nic
p = ((cash % qtr) % dm) % nic

# print total number of least coins
x = q + d + n + p
print(x)