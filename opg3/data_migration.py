from os import path
import csv


def write_row(
    row: list[str], target_file: str, used_ids: list[int], mode: str = "a"
) -> None:
    try:
        with open(target_file, mode, newline="") as target_file:
            if row is None:
                return
            csv_writer = csv.writer(target_file)
            csv_writer.writerow(row)

        used_ids.append(int(row[0]))

    except Exception as e:
        print(f"Encountered an exception while writing to {target_file}:\n{e}\n")
        return


def width_correction(row: list[str], expected_width: int, index: int) -> None:
    if row.count("") >= len(row) - expected_width:
        for _ in range(len(row) - expected_width):
            row.remove("")
    else:
        print(f"Did not perform width correction on row {index}.\n{row}\n")


def id_correction(row: list[str], index: int, used_ids: list[int]) -> None:
    if index not in used_ids:
        row[0] = f"{index}"
    else:
        print(f"Did not perform index correction on row {index}.\n{row}\n")


def mail_correction(row: list[int], index: int) -> None:
    if row[2] == "":
        return
    for mail_end in ["gmail.com", "yahoo.com", "hotmail.com"]:
        if mail_end in row[2]:
            row[2] = row[2][: row[2].find(mail_end)] + "@" + mail_end
            return
    print(f"Did not perform mail correction on row {index}.\n{row}\n")


def error_handling(
    row: list[str], index: int, used_ids: list[int], expected_width: int
) -> list[str]:

    # Removes empty rows
    if len(row) == row.count(""):
        return None

    if len(row) != expected_width:
        width_correction(row, expected_width, index)

    if row[0] != f"{index}":
        id_correction(row, index, used_ids)

    if row[1].count(" ") > 1:
        row[1] = row[1].strip()

    if "@" not in row[2]:
        mail_correction(row, index)

    if (row[1] == "") and (row[2] != ""):
        name: list[str] = row[2][: row[2].find("@")].split(".")
        row[1] = " ".join(name).title()

    try:
        purchase_amount: float = float(row[3])
        if purchase_amount < 0:
            row[3] = row[3].lstrip("-")
    except:
        row[3] = ""

    return row


def migrate_data(
    target_file: str,
    source_file: str = path.join("Data", "source_data.csv"),
) -> None:
    try:
        with open(source_file) as csv_file:
            csv_as_list = list(csv.reader(csv_file))
            used_ids: list[int] = []
            expected_width: int = len(csv_as_list[0])

            write_row(csv_as_list[0], target_file, used_ids, "w")

            for index, row in enumerate(csv_as_list[1:]):
                corrected_row = error_handling(row, index + 1, used_ids, expected_width)
                write_row(corrected_row, target_file, used_ids)

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
