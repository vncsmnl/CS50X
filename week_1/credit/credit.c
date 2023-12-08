#include <cs50.h>
#include <math.h>
#include <stdio.h>

int get_first_n_digits(long long card_number, int n)
{
    {
        while (card_number >= pow(10, n))
            card_number /= 10;
    }
    return card_number;
}

int main(void)
{
    long long card_number = get_long("Number: ");
    int sum = 0;
    int digits = 0;
    int first_two_digits = get_first_n_digits(card_number, 2);

    if (card_number < 1e12)
    {
        printf("INVALID\n");
        return 0;
    }

    while (card_number > 0)
    {
        int last_digit = card_number % 10;

        if (digits % 2 == 0)
        {
            sum += last_digit;
        }
        else
        {
            int doubled = last_digit * 2;
            sum += doubled / 10 + doubled % 10;
        }

        card_number /= 10;
        digits++;
    }

    if (sum % 10 == 0)
    {
        if ((first_two_digits == 34 || first_two_digits == 37) && digits == 15)
        {
            printf("AMEX\n");
        }
        else if ((first_two_digits >= 51 && first_two_digits <= 55) && digits == 16)
        {
            printf("MASTERCARD\n");
        }
        else if ((first_two_digits / 10 == 4) && (digits == 13 || digits == 16))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}
