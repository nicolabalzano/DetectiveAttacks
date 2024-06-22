import json
import os



def read_from_json(path: str, filename: str):
    return json.loads(read_from_file(path, filename + '.json'))


def read_from_file(path: str, filename: str):
    with open(f"{path}{filename}", "r", encoding='utf-8') as file:
        return file.read()


def save_to_json_file(json_data, filename, path):
    json_string = json.dumps(json_data, indent=4, default=str)
    write_to_file(json_string, f"{filename}.json", path)


def check_exist_file_json(filename, path):
    return os.path.isfile(path + filename + '.json')


def write_to_file(file_content, filename, path):
    with open(f"{path}{filename}", "w", encoding='utf-8') as outfile:
        outfile.write(file_content)


def extension_check(filename: str, extension_to_check) -> bool:
    _, extension = os.path.splitext(filename)
    return extension.lower() == extension_to_check

