from os import path


def log_filter(
    filter: str,
    data_folder: str = "Data",
    filename: str = "app_log (logfil analyse) - random.txt",
) -> None:

    filename: str = path.join(data_folder, filename)
    try:
        with open(filename) as names_raw:
            log_list: list[str] = names_raw.readlines()

    except FileNotFoundError:
        print(f"Error: File {filename} not found!")
        return

    filtered_events: list = []
    for event in log_list:
        if filter in event:
            filtered_events.append(event)

    with open(path.join("opg2", f"app_log_{filter}.txt"), "w") as filtered_file:
        filtered_file.writelines(filtered_events)


if __name__ == "__main__":
    filter: str = input(
        "Keyword to filter logs by ex. 'WARNING' or 'ERROR' (not case sensitive) "
    ).upper()
    log_filter(filter)
