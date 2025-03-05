from string import ascii_lowercase as alphabet
from collections import defaultdict


def letter_counter(filename: str = "Data/Navne_liste.txt") -> defaultdict[str, int]:
    try:
        with open(filename) as names_raw:
            names_list: list[str] = names_raw.read().lower()

    except FileNotFoundError:
        print(f"Error: File {filename} not found!")
        return

    letter_count_dict: defaultdict = defaultdict(lambda: 0)
    for letter in alphabet:
        letter_count_dict[letter] = names_list.count(letter)

    return letter_count_dict


if __name__ == "__main__":
    letter_count_dict = letter_counter()

    print(letter_count_dict)
    print(f"Default value test: {letter_count_dict["æ"] = }")
