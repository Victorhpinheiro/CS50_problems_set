#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    //declaring variables

    //check if it has only two arguments and that the length is correct
    if (argc == 2)
    {
        //handle not 26 key
        if (strlen(argv[1]) != 26)
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }

        if (strlen(argv[1]) == 26)
        {
            //handle duplicates and wrong caraters
            for (int i = 0, n= strlen(argv[1]); i < n; i++)
            {
                if ((argv[1][i] < 'a' || argv[1][i] > 'z') && (argv[1][i] < 'A' || argv[1][i] > 'Z'))
                {
                printf("not valid character.\n");
                return 1;
                }
                for (int p = 0, m = strlen(argv[1]); p < m; p++)
                    {
                        if (argv[1][i] == argv[1][p] && p != i)
                        {
                        printf("double character.\n");
                        return 1;
                        }
                    }
            }


            //after no error, get input from user+
            string s = get_string("plaintext:");

            printf("ciphertext:");
            //interate to every key that they offer
            for (int i = 0, n = strlen(s); i < n; i++)
            {
                if (islower(s[i]))
                {
                    for (int x = 'a'; x <= 'z'; x++)
                    {
                        if (s[i] == x)
                        {
                            char subl = tolower(argv[1][x - 'a']);
                            printf("%c", subl);

                        }
                    }
                }
                if (isupper(s[i]))
                {
                    for (int x = 'A'; x <= 'Z'; x++)
                    {
                        if (s[i] == x)
                        {
                            char subu = toupper(argv[1][x - 'A']);
                            printf("%c", subu);
                        }
                    }
                }
                if ((s[i] < 'a' || s[i] > 'z') && (s[i] < 'A' || s[i] > 'Z'))
                {
                    printf("%c", s[i]);
                }
            }
            printf("\n");
            return 0;
        }
    }

    else
    {
        printf("Usage: ./substitution key");
        return 1;
    }

}