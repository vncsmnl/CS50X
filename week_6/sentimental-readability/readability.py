from cs50 import get_string


def calculate_index(letters, words, sentences):
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    return round(index)


def main():
    text = get_string("Text: ")

    letters = sum(c.isalpha() for c in text)
    words = text.count(" ") + 1  # Assuming there is at least one word in the input
    sentences = text.count(".") + text.count("!") + text.count("?")

    grade = calculate_index(letters, words, sentences)

    if grade >= 16:
        print("Grade 16+")
    elif grade < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {grade}")


if __name__ == "__main__":
    main()
