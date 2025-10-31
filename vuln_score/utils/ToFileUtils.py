import json


def save_to_json_file(json_data: dict, filename: str, path: str):
    json_string = json.dumps(json_data, indent=4, default=str)
    __write_to_file__(json_string, filename, path)


def save_string_to_file(string: str, filename: str, path: str):
    __write_to_file__(string, filename, path)


def __write_to_file__(file_content: str, filename: str, path: str):
    with open(f"{path}{filename}", "w") as outfile:
        outfile.write(file_content)


def get_json_from_file(filename: str, path: str):
    with open(f"{path}{filename}", "r", encoding='utf-8') as file:
        return json.load(file)
