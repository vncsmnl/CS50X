#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // Prompt the user for input
    string text = get_string("Text: ");

    // Initialize variables to count letters, words, and sentences
    int letter_count = 0;
    int word_count = 1; // Initialize to 1 since the first word doesn't have a space before it
    int sentence_count = 0;

    // Iterate through the input text
    for (int i = 0; i < strlen(text); i++)
    {
        char c = text[i];

        if (isalnum(c))
        {
            letter_count++;
        }
        else if (c == ' ')
        {
            word_count++;
        }
        else if (c == '.' || c == '?' || c == '!')
        {
            sentence_count++;
        }
    }

    // Calculate L and S values
    float L = (float) letter_count / (float) word_count * 100;
    float S = (float) sentence_count / (float) word_count * 100;

    // Calculate the Coleman-Liau index
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Print the corresponding grade level
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

    return 0;
}
