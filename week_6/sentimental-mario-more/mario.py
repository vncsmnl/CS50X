from cs50 import get_int


def get_valid_height():
    while True:
        height = get_int("Height: ")
        if 1 <= height <= 8:
            return height
        else:
            print("Please enter a height between 1 and 8.")


def print_pyramid(height):
    for i in range(1, height + 1):
        spaces = " " * (height - i)
        blocks = "#" * i
        print(f"{spaces}{blocks}  {blocks}")


def main():
    height = get_valid_height()
    print_pyramid(height)


if __name__ == "__main__":
    main()
