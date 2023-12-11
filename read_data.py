import tarfile
import json


class Read_data:

    def __init__(self, path_to_file=None, path_to_extract=None):
        self.path_to_file = path_to_file
        self.path_to_extract = path_to_extract

    def read_tar_file(self):
        with tarfile.open(self.path_to_file) as tar:
            tar.extractall(self.path_to_extract)

    def read_meta(self):
        with open(self.path_to_file + '/fields.json') as json_file:
            meta = json.load(json_file)
        return meta

    def read_label(self):
        with open(self.path_to_file + '/label', 'r') as f:
            label = f.readline()
        return label
