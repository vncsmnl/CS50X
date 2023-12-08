#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ALPHABET_SIZE 26

bool is_positive_integer(string s);

int main(int argc, string argv[])
{
    if (argc != 2 || !is_positive_integer(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int k = atoi(argv[1]);
    string text = get_string("Text: ");
    printf("ciphertext: ");

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            if (isupper(text[i]))
            {
                char cipher_num_capital = ((text[i] - 'A' + k) % ALPHABET_SIZE) + 'A';
                printf("%c", cipher_num_capital);
            }
            else if (islower(text[i]))
            {
                char cipher_num_small = ((text[i] - 'a' + k) % ALPHABET_SIZE) + 'a';
                printf("%c", cipher_num_small);
            }
        }
        else
        {
            printf("%c", text[i]);
        }
    }

    printf("\n");
    return 0;
}

bool is_positive_integer(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (!isdigit(s[i]))
        {
            return false;
        }
    }
    return true;
}
