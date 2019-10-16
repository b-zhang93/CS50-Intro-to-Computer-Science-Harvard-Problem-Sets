This week we were to use C to create two different ciphers. It would scramble the user inputted messaged based on the 
cipher and output the encrypted message.

Caesar:
Using the old caesarian cipher technique, users will select a "key" integer. The key how many places each character of the inputted message
will shift. For example if key is 4 an the input is A ... the output will be E which is 4 places from A. The program also loops back around after Z and starts at A again.
It also ignores spaces and special characters. 

Vigenere:
Elaborates upon Caesarian technique where the "key" is now a string. For each character of the key string, the user inputted message will be scrambled by corresponding character of the key.
For example if the key is ABC  and the input is HELLO, then H gets shifted by the value of A (which is 0), E gets shifted by value of B (which is 1), L shifts by C (2), L again by A (0), and O by B(2).
So the key rotates until the message is complete. The encrypted message is then outputted for the user. 

Learned:
- argc and argv
- command line arguments
- nested if  and for loops
- various string related functions (isupper, islower, isalpha, etc..)
- arrays and iterations of arrays in for loops
- ascii table and how to alter strings based on their ascii values to int and back to string for output
- algorithmic logic
