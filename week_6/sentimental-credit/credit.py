from cs50 import get_string
from math import floor

VISA_PREFIX = "4"
AMEX_PREFIXES = ["34", "37"]
MASTERCARD_PREFIXES = ["51", "52", "53", "54", "55"]
INVALID_BRAND = "INVALID"


def clean_input(card_number):
    return card_number.strip()


def get_card_brand(card_number):
    if card_number.startswith(VISA_PREFIX) and len(card_number) == 13:
        return "VISA"
    elif card_number[:2] in AMEX_PREFIXES and len(card_number) == 15:
        return "AMEX"
    elif card_number[:2] in MASTERCARD_PREFIXES and len(card_number) == 16:
        return "MASTERCARD"
    elif card_number.startswith(VISA_PREFIX) and len(card_number) == 16:
        return "VISA"
    else:
        return INVALID_BRAND


def is_valid_card(card_number):
    card_number = int(card_number)
    last = 0
    temp = 0
    sec_to_last = 0

    while card_number > 0:
        last += card_number % 10
        card_number //= 10

        temp = (card_number % 10) * 2

        if temp >= 10:
            sec_to_last += temp % 10
            temp //= 10
            sec_to_last += floor(temp)
        else:
            sec_to_last += temp

        card_number //= 10

    return (last + sec_to_last) % 10 == 0


def main():
    card_number = get_string("Number: ")
    card_number = clean_input(card_number)
    brand = get_card_brand(card_number)

    if brand != INVALID_BRAND:
        if is_valid_card(card_number):
            print(brand)
        else:
            print(INVALID_BRAND)
    else:
        print(INVALID_BRAND)


if __name__ == "__main__":
    main()
