#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

#define NUM_BUCKETS 5381

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Hash table
node *table[NUM_BUCKETS] = {NULL};

// Words in the dictionary
unsigned int dictionaryWords = 0;

// Hash code from the word
unsigned int hashCode = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    hashCode = hash(word);
    node *currentWordNode = table[hashCode];

    while (currentWordNode != NULL)
    {
        if (strcasecmp(currentWordNode->word, word) == 0)
        {
            return true;
        }
        currentWordNode = currentWordNode->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c;

    while ((c = tolower(*word++)))
    {
        hash = ((hash << 5) + hash) + c;
    }
    return hash % NUM_BUCKETS;
}

// Insert a word into the hash table
void insertWord(const char *word)
{
    node *n = malloc(sizeof(node));

    if (n != NULL)
    {
        hashCode = hash(word);
        strcpy(n->word, word);
        n->next = table[hashCode];
        table[hashCode] = n;
        dictionaryWords++;
    }
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];
    FILE *dic = fopen(dictionary, "r");

    if (dic == NULL)
    {
        return false;
    }

    while (fscanf(dic, "%s", word) != EOF)
    {
        insertWord(word);
    }

    fclose(dic);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dictionaryWords;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < NUM_BUCKETS; i++)
    {
        node *currentNode = table[i];

        while (currentNode)
        {
            node *tmp = currentNode;
            currentNode = currentNode->next;
            free(tmp);
        }
    }

    return true;
}
