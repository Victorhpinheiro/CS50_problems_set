#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //right number of arguments
    if (argc != 2)
    {
        printf("wrong usage, usage: ./recover <file>");
        return 1;
    }
    //Open the file input
    FILE *infile = fopen(argv[1], "r");
    if (infile == NULL)
    {
        printf("Could not open input\n");
        return 1;
    }


    //looking beging of JPEG bytes are 0xff 0xd8 0xff 0xe*
    BYTE bytes[512];
    int count = 0;
    char *name = malloc(8 * sizeof(char));
    FILE *output = NULL;

    while(fread(&bytes, 1, 512, infile))
    {

        if(bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && (bytes[3] & 0xf0) == 0xe0)
        {
            if (count != 0)
            {
                fclose(output);
            }
            sprintf(name, "%03i.jpg", count);
            output = fopen(name, "w");
            count++;
            if (output == NULL)
            {
                printf("Could not open output\n");
                return 1;
            }
        }

        if (output !=NULL)
        {
              fwrite(&bytes, 1, 512, output);
        }
    }
    free(name);
    fclose(output);
    fclose(infile);
    return 0;
}