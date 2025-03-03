sorting_method: str = input(
    "Accepts 'a' for alphabetical sorting and 'l' for sorting by length or 'al' for both."
)


def sort_names(sorting_method: str, filename: str = "Data/Navne_liste.txt") -> None:
    if sorting_method not in ["a", "l", "al"]:
        print("Error: Invalid sorting method!")
        return

    try:
        with open(filename) as names_raw:
            names_list: list[str] = names_raw.read().split(",")

    except FileNotFoundError:
        print(f"Error: File {filename} not found!")
        return

    if "a" in sorting_method:
        names_list.sort()  # sorts names alphabetically
    if "l" in sorting_method:
        names_list.sort(key=str.__len__)  # sorts names by length

    print(names_list)


if __name__ == "__main__":
    sort_names(sorting_method=sorting_method)
