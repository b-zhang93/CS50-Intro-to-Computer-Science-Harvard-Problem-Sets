#include <stdio.h>
#include <cs50.h>
#include <math.h>

int get_pos_float(string prompt);

int main(void)
{
    int qtr = 25;
    int dm = 10;
    int nic = 5;
    int pen = 1;
    int c = get_pos_float("Change Owed: ");
    int count = 0;
    while (c >= qtr)
    {
        count++;
        c -= qtr;
    }
    while(c >= dm)
    {
        count++;
        c-=dm;
    }
    while(c >= nic)
    {
        count++;
        c-=nic;
    }
    while(c >= pen)
    {
        count++;
        c-=pen;
    }
    printf("%i\n", count);
}

int get_pos_float(string prompt)
{
    float n;
    do
    {
         n = round(get_float("%s", prompt) * 100);
    }
    while (n < 0);
    return n;
}
