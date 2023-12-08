#include "helpers.h"
#include <math.h>

// Helper function to round and clamp a value between 0 and 255
int clamp(int value)
{
    return fmin(255, fmax(0, round(value)));
}

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float avg = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0;
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = clamp(avg);
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int original_red = image[i][j].rgbtRed;
            int original_green = image[i][j].rgbtGreen;
            int original_blue = image[i][j].rgbtBlue;
            float sepia_red = 0.393 * original_red + 0.769 * original_green + 0.189 * original_blue;
            float sepia_green = 0.349 * original_red + 0.686 * original_green + 0.168 * original_blue;
            float sepia_blue = 0.272 * original_red + 0.534 * original_green + 0.131 * original_blue;
            image[i][j].rgbtRed = clamp(sepia_red);
            image[i][j].rgbtGreen = clamp(sepia_green);
            image[i][j].rgbtBlue = clamp(sepia_blue);
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            int opposite = width - 1 - j;
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][opposite];
            image[i][opposite] = tmp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a temporary copy to avoid modifying the original image
    RGBTRIPLE copy[height][width];
    memcpy(copy, image, sizeof(RGBTRIPLE) * height * width);

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red_sum = 0, green_sum = 0, blue_sum = 0, divisor = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    if (ni >= 0 && nj >= 0 && ni < height && nj < width)
                    {
                        red_sum += copy[ni][nj].rgbtRed;
                        green_sum += copy[ni][nj].rgbtGreen;
                        blue_sum += copy[ni][nj].rgbtBlue;
                        divisor++;
                    }
                }
            }

            image[i][j].rgbtRed = clamp((float)red_sum / divisor);
            image[i][j].rgbtGreen = clamp((float)green_sum / divisor);
            image[i][j].rgbtBlue = clamp((float)blue_sum / divisor);
        }
    }
}
