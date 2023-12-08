#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check for invalid usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s forensic_image\n", argv[0]);
        return 1;
    }

    // Open the forensic image file
    FILE *file = fopen(argv[1], "rb");
    if (file == NULL)
    {
        perror("Could not open file");
        return 1;
    }

    // Create a buffer to read from the forensic image
    BYTE buffer[BLOCK_SIZE];

    // Initialize the file counter for the number of JPGs found
    int file_counter = 0;

    // Initialize the output file pointer to NULL
    FILE *output_file = NULL;

    // Read blocks of 512 bytes from the file until the end
    while (fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        // Check for the beginning of a JPG file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (output_file != NULL)
            {
                fclose(output_file);
            }
            // Create a JPG file
            char file_name[12];
            snprintf(file_name, sizeof(file_name), "%03i.jpg", file_counter);
            output_file = fopen(file_name, "wb");
            if (output_file == NULL)
            {
                perror("Could not open file");
                return 1;
            }
            file_counter++;
        }

        // Write the block with the JPG image to the output file
        if (output_file != NULL)
        {
            fwrite(buffer, BLOCK_SIZE, 1, output_file);
        }
    }

    // Close the output file if it's open
    if (output_file != NULL)
    {
        fclose(output_file);
    }

    // Close the forensic image file
    fclose(file);

    return 0;
}
