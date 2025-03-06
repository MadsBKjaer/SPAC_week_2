from os import path
import csv


def write_row(
    row: list[str], target_file: str, used_ids: list[str], mode: str = "a"
) -> None:
    try:
        with open(target_file, mode, newline="") as target_file:
            if row is None:
                return
            csv_writer = csv.writer(target_file)
            csv_writer.writerow(row)

        used_ids.append(row[0])  # Store used ids to avoid duplicates

    except Exception as e:
        print(f"Encountered an exception while writing to {target_file}:\n{e}\n")
        return


def width_correction(row: list[str], expected_width: int) -> None:
    extra_width: int = len(row) - expected_width
    empty_cells: int = row.count("")

    if min(extra_width, empty_cells) == 0:
        return ""

    old_width: int = len(row)
    for _ in range(min(extra_width, empty_cells)):
        row.remove("")
    return f"Empty cell: Removed {old_width - len(row)} cell(s). "


def id_correction(row: list[str], index: int, used_ids: list[str]) -> str:
    if (row[0] == str(index)) or (str(index) in used_ids):
        return ""

    old_id: str = row[0]
    row[0] = str(index)
    return f"Id: {repr(old_id)} -> {repr(row[0])}. "


def mail_correction(row: list[int]) -> str:
    if row[2] == "":
        return ""
    if "@" in row[2]:
        return ""

    old_mail: str = row[2]

    for mail_domain in ["gmail.com", "yahoo.com", "hotmail.com"]:
        if mail_domain in row[2]:
            row[2] = row[2][: row[2].find(mail_domain)] + "@" + mail_domain
            return f"Mail: {repr(old_mail)} -> {repr(row[2])}. "


def name_correction(row: list[int]) -> str:
    change_message: str = ""
    if row[1].startswith(" ") or row[1].endswith(" "):
        old_name: str = row[1]
        row[1] = row[1].strip()
        change_message += f"Name: {repr(old_name)} -> {repr(row[1])}. "

    # Name correction using mail. (different log message)
    if (row[1] == "") and (row[2] != ""):
        name: list[str] = row[2][: row[2].find("@")].split(".")
        row[1] = " ".join(name).title()
        change_message += f"Name from mail: {repr(row[1])} from {repr(row[2])}. "

    return change_message


def purchase_amount_correction(row: list[int]) -> str:
    if row[3] == "":
        return ""
    if "-" not in row[3] and all(
        character.isnumeric() for character in row[3].replace(".", "")
    ):
        return ""

    old_purchase_amount: str = row[3]

    if any(character.isalpha() for character in row[3]):
        row[3] = ""

    if "-" in row[3]:
        row[3] = row[3].lstrip("-")

    return f"Purchase amount: {repr(old_purchase_amount)} -> {repr(row[3])}. "


def error_handling(
    row: list[str],
    index: int,
    used_ids: list[str],
    expected_width: int,
    changes_list: list[list[str]],
) -> list[str]:

    # Removes empty rows
    if len(row) == row.count(""):
        changes_list.append(f"Line {index:5} changes: Empty cell: Removed line.\n")
        return None

    changes_made: str = f"Line {index:5} changes: "

    changes_made += width_correction(row, expected_width)
    changes_made += id_correction(row, index, used_ids)
    changes_made += mail_correction(row)
    changes_made += name_correction(row)
    changes_made += purchase_amount_correction(row)

    if changes_made != f"Line {index:5} changes: ":
        changes_list.append(changes_made + "\n")

    return row


def migrate_data(
    target_file: str,
    source_file: str = path.join("Data", "source_data.csv"),
) -> None:

    used_ids: list[int] = []
    changes_list: list[list[str]] = []

    try:
        with open(source_file) as csv_file:
            csv_as_list = list(csv.reader(csv_file))
            expected_width: int = len(csv_as_list[0])

            write_row(csv_as_list[0], target_file, used_ids, "w")
            for index, row in enumerate(csv_as_list[1:]):
                corrected_row = error_handling(
                    row, index + 1, used_ids, expected_width, changes_list
                )
                write_row(corrected_row, target_file, used_ids)

        with open(path.join("opg3", f"changes_log.txt"), "w") as changes_file:
            changes_file.writelines(changes_list)

    except FileNotFoundError:
        print(f"Error: File {source_file} not found!")


def filter_incomplete_data(target_file: str, source_file: str) -> None:
    try:
        with open(source_file) as csv_file:
            csv_as_list = list(csv.reader(csv_file))
            used_ids: list[int] = []
            write_row(csv_as_list[0], target_file, used_ids, "w")

            for index, row in enumerate(csv_as_list[1:]):
                if "" in row:
                    continue
                write_row(row, target_file, used_ids)
    except FileNotFoundError:
        print(f"Error: File {source_file} not found!")


if __name__ == "__main__":
    corrected_path: str = path.join("opg3", "corrected_data.csv")
    migrate_data(corrected_path)
    complete_path: str = path.join("opg3", "complete_data.csv")
    filter_incomplete_data(complete_path, corrected_path)
