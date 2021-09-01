#include<cs50.h>
#include<stdio.h>
#include<string.h>
#include<math.h>


int main(void)
{
    //get string
    string s = get_string("Text: ");

    //declare variables
    int espaces = 0;
    int letters = 0;
    int words = 0;
    int sent = 0;

    //go to every character and feed the variables correctly
    for(int i=0, n=strlen(s); i < n; i++)
    {
        if((s[i] >= 'a' && s[i] <= 'z') || (s[i] >= 'A' && s[i] <= 'Z'))
        {
            letters += 1;
        }

        if (s[i] == 32)
        {
            espaces += 1;
        }

        if (s[i] == '.' || s[i] == '!' || s[i] == '?')
        {
            sent += 1;
        }
    }

    //determine the number of words
    words = espaces + 1;

    float L = (letters * 100) / words;
    float S = (100 * sent) / words;
    float ind = 0.0588 * L - 0.296 * S - 15.8;
    int index = round(ind);

    //print results
    if (ind < 2)
    {
        printf("Before Grade 1\n");
    }
    if (ind > 16)
    {
        printf("Grade 16+\n");
    }
    if (ind>2 && ind<16)
    {
        printf("Grade %i\n", index);
    }
}