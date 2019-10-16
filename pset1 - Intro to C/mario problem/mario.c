#include <cs50.h>
#include <stdio.h>

int get_positive_int(string prompt);

int main(void)
{
    int h = get_positive_int("Height: ");
   
    for (int l = 0; l < h; l++)
    {
        int x = l+1;
        for(int d = l + 1; d < h; d++)
        {
            printf(" ");
        }
            for (int i = l; i < l + x; i++)
            {
                printf("#");
            }
        printf("\n");
    }
}

int get_positive_int(string prompt)
{
    int n;
    do
    {
        n = get_int("%s", prompt);
    }
    while (n < 1 || n > 8);
    return n;
}
