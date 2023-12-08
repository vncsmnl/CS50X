#include "helpers.h"

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    // Define the color to change black pixels to
    RGBTRIPLE blackToColor;
    blackToColor.rgbtRed = 0x56;
    blackToColor.rgbtGreen = 0xBF;
    blackToColor.rgbtBlue = 0x2C;

    // Loop through the image pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Check if the pixel is black
            if (image[i][j].rgbtRed == 0x00 && image[i][j].rgbtGreen == 0x00 && image[i][j].rgbtBlue == 0x00)
            {
                // Change the black pixel to the specified color
                image[i][j] = blackToColor;
            }
        }
    }
}
