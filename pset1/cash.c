#include <stdio.h>
#include <cs50.h>


int main(void)
{
    //defining the variables and get positive float less than 1
    float change;
    int coins = 0;
    do
    {
        change = get_float("How much do you want to chage? ");
    }
    while (change <= 0);

    //check if the coins is bigger than the coins and add to count while removing when bigger
    while (change > 0.009)
    {
        if (change >= 0.25)
        {
            coins = coins + 1;
            change = change - 0.25;
            printf("the coins is %i and change are %f\n", coins, change);
        }
        if (change >= 0.10 && change < 0.25)
        {
            coins = coins + 1;
            change = change - 0.10;
            printf("the coins is %i and change are %f\n", coins, change);
        }
        if (change >= 0.05 && change < 0.10)
        {
            coins = coins + 1;
            change = change - 0.05;
            printf("the coins is %i and change are %f\n", coins, change);
        }
        if (change > 0.009 && change < 0.05)
        {
            coins = coins + 1;
            change = change - 0.01;
            printf("the coins is %i and change are %f\n", coins, change);
        }
    }
    printf("%i\n", coins);
}