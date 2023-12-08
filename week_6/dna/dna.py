import csv
import argparse


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Find matching profiles in DNA data.")
    parser.add_argument("data_file", help="CSV file containing DNA data")
    parser.add_argument("sequence_file", help="File containing DNA sequence")
    args = parser.parse_args()

    # Read database into memory
    with open(args.data_file, newline="") as file:
        reader = csv.reader(file)
        header, *database = reader
        database = {row[0]: list(map(int, row[1:])) for row in database}

    # Read DNA sequence into memory
    with open(args.sequence_file) as dna_file:
        dna = dna_file.read()

    # Compute longest run of consecutive STR repeats
    lengths = [longest_match(dna, subseq) for subseq in header[1:]]

    # Check database for matching profiles
    for person, profile in database.items():
        if profile == lengths:
            print(person)
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    sublen = len(subsequence)
    longest = 0

    for i in range(len(sequence)):
        count = 0
        while sequence[i + count * sublen : i + (count + 1) * sublen] == subsequence:
            count += 1

        longest = max(longest, count)

    return longest


if __name__ == "__main__":
    main()
