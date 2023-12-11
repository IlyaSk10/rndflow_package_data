import os
import json


def get_from_json(json_path):
    try:
        json_path = os.path.abspath(json_path)
        with open(json_path) as json_file:
            data = json.load(json_file)
    except FileNotFoundError as e:
        print(f'File not found: {json_path}')
        return None
    return data


def extract_tarfile(filename=None, save_to=None):
    import tarfile

    if filename==None or not filename:
        return
    if save_to is None or not save_to:
        save_to = os.path.dirname(filename)
    if filename.endswith('.tar.gz'):
        with tarfile.open(filename, "r:gz") as tar:
            tar.extractall(path=save_to)
    elif filename.endswith('.tar'):
        with tarfile.open(filename, "r") as tar:
            tar.extractall(path=save_to)


if __name__ == "__main__":
    filename = 'saved/1409644.tar'
    extract_tarfile(filename=filename, save_to="saved")
    ...
