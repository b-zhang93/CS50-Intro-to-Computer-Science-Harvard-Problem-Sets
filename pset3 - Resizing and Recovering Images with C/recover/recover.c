#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    //save and open input file
    char *infile  = argv[1];
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 2;
    }

    FILE *img;
    uint8_t buffer[512]; //buffer
    int count = 0;  // counter for files


    while (fread(buffer, 512, 1, inptr))
    {

        //checks for header for JPG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //creates a file with file name counting up from 000
            char filename[8];
            sprintf(filename, "%03d.jpg", count);
            img = fopen(filename, "w");
            count++;

            //checks if new file is usable
            if (img == NULL)
            {
                fclose(inptr);
                fprintf(stderr, "Usage: ./recover image\n");
                return 3;
            }
        }

        //write to the new file
        if (img != NULL)
        {
            fwrite(&buffer, 512, 1, img);
        }
    }

    //closes files
    fclose(img);
    fclose(inptr);

    printf("found %i images\n", count);
    return 0;
}
