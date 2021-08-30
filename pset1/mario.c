#include <cs50.h>
#include <stdio.h>

int main(void)
{   //get positive integer between 1 and 8
    int h;
    do
    {
        h = get_int("height? ");
    }
    while(h < 1 || h > 8);


    //print the blocks
    for (int i = 0; i < h; i++)
    {
        for (int space = 1; space < (h-i)  ; space++)
        {
            printf(" ");
        }

        for (int brink = 0; brink < (i+1); brink++)
        {
            printf("#");
        }
        printf("  ");
        for (int brink = 0; brink < (i+1); brink++)
        {
            printf("#");
        }
        printf("\n");
    }
}