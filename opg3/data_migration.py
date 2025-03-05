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
    for mail_end in ["gmail.com", "yahoo.com", "hotmail.com"]:
        if mail_end in row[2]:
            row[2] = row[2][: row[2].find(mail_end)] + "@" + mail_end
            return
    print(f"Did not perform mail correction on row {index}.\n{row}\n")


def error_handling(
    row: list[str],
    index: int,
    used_ids: list[int],
    expected_width: int,
    changes_list: list[list[str]],
) -> list[str]:

    # Removes empty rows
    if len(row) == row.count(""):
        changes_list.append(f"Line {index:5} changes: Empty cell: Removed line.\n")
        return None

    changes_made: str = f"Line {index:5} changes: "

    if len(row) != expected_width:
        old_width: int = len(row)
        width_correction(row, expected_width, index)
        changes_made += f"Empty cell: Removed {old_width - expected_width} cell(s). "

    if row[0] != f"{index}":
        old_id: str = row[0]
        id_correction(row, index, used_ids)
        changes_made += f"Id: {repr(old_id)} -> {repr(row[0])}. "

    if row[1].startswith(" ") or row[1].endswith(" "):
        old_name: str = row[1]
        row[1] = row[1].strip()
        changes_made += f"Name: {repr(old_name)} -> {repr(row[1])}. "

    if ("@" not in row[2]) and (not row[2] == ""):
        old_mail: str = row[2]
        mail_correction(row, index)
        changes_made += f"Mail: {repr(old_mail)} -> {repr(row[2])}. "

    if (row[1] == "") and (row[2] != ""):
        name: list[str] = row[2][: row[2].find("@")].split(".")
        row[1] = " ".join(name).title()
        changes_made += f"Name from mail: {repr(row[1])} from {repr(row[2])}. "

    try:
        purchase_amount: float = float(row[3])
        if purchase_amount < 0:
            old_purchase_amount: str = row[3]
            row[3] = row[3].lstrip("-")
            changes_made += (
                f"Purchase amount: {repr(old_purchase_amount)} -> {repr(row[3])}. "
            )
    except:
        old_purchase_amount: str = row[3]
        row[3] = ""
        changes_made += (
            f"Purchase amount: {repr(old_purchase_amount)} -> '{repr(row[3])}'. "
        )

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
