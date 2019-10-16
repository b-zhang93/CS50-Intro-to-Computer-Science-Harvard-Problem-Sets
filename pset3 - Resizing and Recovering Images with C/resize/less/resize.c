#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <string.h>
#include "bmp.h"



int main(int argc, char *argv[])
{
    // checks for right amoung of arguments
    if (argc != 4)
    {
        printf("Usage1: ./resize n infile outfile\n");
        return 1;
    }

    // sets a few variables for n, infile, outfile
    // int n = get_int("%s", argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];
    int n = atoi(argv[1]);

    // checks if n input is within accepted range
    if (n > 100 || n < 0)
    {
        printf("Usage2: ./resize n infile outfile\n");
        return 2;
    }

    // input file and check
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Usage3: ./resize n infile outfile\n");
        return 3;
    }

    // open output file and check
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        printf("Usage4: ./resize n infile outfile\n");
        return 4;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    int oldpadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    bi.biWidth *= n;
    bi.biHeight *= n;

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + padding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);


    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight / n); i < biHeight; i++)
    {
        // creating an array to store pixels n times and count for array position
        RGBTRIPLE narray[bi.biWidth];
        int count = 0;

        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth / n; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // write triple to array n times
            for (int m = 0; m < n; m++, count++)
            {
                narray[count] = triple;
            }

        }

        //read from array and output n times for each row
        for (int l = 0; l < n; l++)
        {
            fwrite(&narray, sizeof(narray), 1, outptr);

            // padding
            for (int k = 0; k < padding; k++)
            {
                fputc(0x00, outptr);
            }
        }

        // skip over padding, if any
        fseek(inptr, oldpadding, SEEK_CUR);
    }
    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    return 0;
}


