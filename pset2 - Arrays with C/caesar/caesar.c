#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    //variables for command argument, conversion of it to integer value, and length of argument
    string s = argv[1];
    int k = atoi(argv[1]);
    int n = strlen(argv[1]);
    
    //exit if not 2 arguments       
    if (argc != 2 || argc < 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
   
    //exit for non integer character in the argument 
    for (int i = 0; i < n; i++)
    {
        if (!isdigit(s[i]))
        {   
            printf("Usage: ./caesar key\n");
            return 1;
        }   
    }
    
    //prompt for plaintext and output ciphertext based on argv[1] key
    string pt = get_string("plaintext: ");      
    printf("ciphertext: ");
    
    //for loop to check each value, change it, and print it out based on key value
    for (int i = 0, x = strlen(pt); i < x; i++)
    {
        //for lower case letters maintain lowercase and check if needs to loop
        if (islower(pt[i]) && isalpha(pt[i]))
        {
            //checks if the value value needs to be looped around or not if true = no need to loop
            if (122 - pt[i] >= k)
            {
                char y = pt[i] + k;
                printf("%c", tolower(y));
            }
            else
            {
                //makes value start from beginning of the alphabet to loop 
                // pt[i] - 96 determines letter position between 1-26 for lower case letters based on their ascii value   
                int m = ((pt[i] - 96) + k) % 26;
                char y = 96 + m;
                printf("%c", tolower(y));
            }
        }
        else
        {
            //makes sure uppercase is kept and capital letters are looped as well
            if (isupper(pt[i]) && isalpha(pt[i]))
            {
                if (90 - pt[i] >= k)
                {
                    char y = pt[i] + k;
                    printf("%c", toupper(y));  
                }
                else
                {
                    int m = ((pt[i] - 64) + k) % 26;
                    char y = 64 + m;
                    printf("%c", toupper(y));
                }            
            }   
            //makes sure punctuation and other non alpha chars are maintained the same, only letters are encrypted
            else
            {
                printf("%c", pt[i]);

            }
        }
    }
    printf("\n");
}

