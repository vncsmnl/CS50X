#include <cs50.h>
#include <stdio.h>
#include <string.h>

#define MAX_CANDIDATES 9

// Define a struct for candidates
typedef struct
{
    string name;
    int votes;
} Candidate;

// Function prototypes
bool vote(string name);
void print_winner(void);

// Global array of candidates
Candidate candidates[MAX_CANDIDATES];
int candidate_count = 0;

int main(int argc, string argv[])
{
    // Check for proper usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Check if the number of candidates exceeds the maximum
    if (argc - 1 > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }

    // Populate the candidates array
    candidate_count = argc - 1;
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Process votes
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Print the winner(s)
    print_winner();
}

// Update vote totals for the given candidate
bool vote(string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i].name) == 0)
        {
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

// Print the winner(s) of the election
void print_winner(void)
{
    int max_votes = 0;

    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > max_votes)
        {
            max_votes = candidates[i].votes;
        }
    }

    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes == max_votes)
        {
            printf("%s\n", candidates[i].name);
        }
    }
}
