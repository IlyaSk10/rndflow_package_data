import numpy as np

import requests
import json
import os
import h5py
from urllib import request

from server import Server, response_json
from project import Project
from node import Node
from package import Package
from data_layer import DataLayer
from additional import get_from_json, extract_tarfile
from parameters import Parameters

JSON_PATH = "json_files/"
SITE_PATH = "https://ias.rndflow.com"
PACKAGES_SAVE_PATH = "packages"


class DataMaker:
    def __init__(self):
        self.connect_server()
        self.get_connect_data()
        self.get_project()
        self.get_node()
        self.get_data_layer()
        self.get_package()
        self.set_packages_save_path()
        self.download_packages()
        self.extract_packages()
        self.load_packages_data()
        self.download_node_files()

    def list_params(self):
        self.parameters = Parameters(server=self.server, project_id=self.project.id)
        self.parameters.list_param_values(node_id=self.node.id, data_layer_id=self.data_layer.id)

    def connect_server(self):
        api_key = self.get_access_token(path=JSON_PATH, url=SITE_PATH)
        self.server = Server(api_server=SITE_PATH, api_key=api_key)

    def get_connect_data(self, filepath=None):
        if filepath is None:
            filepath = os.path.join(JSON_PATH, "connect_data.json")
        self.connect_data = get_from_json(filepath)

    def set_packages_save_path(self):
        if not os.path.exists(PACKAGES_SAVE_PATH):
            self.packages_save_path = os.path.join(os.getcwd(), PACKAGES_SAVE_PATH)
            if not os.path.exists(self.packages_save_path):
                os.mkdir(self.packages_save_path)
        else:
            self.packages_save_path = PACKAGES_SAVE_PATH

    def download_packages(self, package_ids=None):
        package_ids = package_ids or self.connect_data["package_ids"]
        self.package.download(save_path=self.packages_save_path, package_ids=package_ids)

    def extract_packages(self, package_ids=None):
        package_ids = package_ids or self.connect_data["package_ids"]
        for package_id in package_ids:  # extract packages from downloaded tar files
            extract_tarfile(filename=os.path.join(self.packages_save_path, f"{package_id}.tar"))

    def load_packages_data(self, package_ids=None):
        package_ids = package_ids or self.connect_data["package_ids"]
        self.packages_data = {}
        for package_id in package_ids:  # read packages data
            self.packages_data[package_id] = self.get_package_data(
                package_id=package_id,
                folderpath=os.path.join(self.packages_save_path, str(package_id)))

    def download_node_files(self):
        self.path_to_node_files = 'files/'
        if not os.path.exists(self.path_to_node_files):
            os.mkdir(self.path_to_node_files)
        node_files = self.server.get(endpoint=f"/projects/{self.project.id}/nodes/{self.node.id}/files")
        for node_file in node_files:
            request.urlretrieve(node_file['content'], self.path_to_node_files + node_file['name'])

    def get_package_data(self, package_id, folderpath):
        data = dict()
        filespath = os.path.join(folderpath, 'files')
        for root, dirs, files in os.walk(filespath):
            for file in files:
                fullpath = os.path.join(root, file)
                if file.endswith('.h5') or file.endswith('.hdf5'):
                    filename = os.path.splitext(file)[0]
                    data.update(self.get_data_from_hdf5(fullpath))
                elif os.path.basename(file) == 'meta.json':
                    with open(fullpath, 'r') as f:
                        data['meta'] = json.load(f)
        fieldspath = os.path.join(folderpath, 'fields.json')
        with open(fieldspath, 'r') as f:
            data['fields'] = json.load(f)
        labelpath = os.path.join(folderpath, 'label')
        with open(labelpath, 'r') as f:
            data['label'] = f.read()
        return data

    @staticmethod
    def get_data_from_hdf5(filepath):
        def convert_hdf5_to_dict(file, name='/'):
            item = file[name]

            if isinstance(item, h5py.Dataset):
                return np.array(item)
            elif isinstance(item, h5py.Group):
                group_dict = {}
                for key in item.keys():
                    group_dict[key] = convert_hdf5_to_dict(file, f'{name}{key}/')
                return group_dict

        with h5py.File(filepath, 'r') as f:
            data_dict = convert_hdf5_to_dict(f)
        return data_dict

    def get_project(self):
        self.project = Project(server=self.server)
        self.select_project(project_name=self.connect_data["project_name"])

    def get_node(self):
        self.node = Node(server=self.server, project_id=self.project.id)
        self.select_node(node_name=self.connect_data["node_name"])

    def get_data_layer(self):
        self.data_layer = DataLayer(server=self.server, project_id=self.project.id)
        self.select_data_layer(data_layer_name=self.connect_data["data_layer_name"])

    def get_package(self):
        self.package = Package(server=self.server, project_id=self.project.id, node_id=self.node.id)
        self.package.search(data_layer_id=self.data_layer.id)

    def extract_data(self, package_ids):
        for package_id in package_ids:
            extract_tarfile(filename=os.path.join(PACKAGES_SAVE_PATH, f"{package_id}.tar"))

    def select_workspace(self, workspace_name):
        workspaces = self.workspace.list_workspaces()
        for workspace in workspaces["items"]:
            if workspace["label"] == workspace_name:
                workspace_id = workspace["id"]
                break
        self.workspace.read(workspace_id=workspace_id)

    def select_project_from_workspace(self, project_name):
        projects = self.workspace.list_projects()
        for project in projects["items"]:
            if project["label"] == project_name:
                project_id = project["id"]
                break
        self.project.read(project_id=project_id)

    def select_project(self, project_name):
        projects = self.project.list_projects()
        for project in projects["items"]:
            if project["label"] == project_name:
                project_id = project["id"]
                break
        self.project.read(project_id=project_id)

    def select_node(self, node_name):
        nodes = self.node.list_nodes(project_id=self.project.id)
        for node in nodes:
            if node["label"] == node_name:
                node_id = node["id"]
                break
        self.node.read(node_id=node_id)

    def select_user(self, user_name):
        users = self.project.list_project_users()
        for user in users:
            if user["user"]["username"] == user_name:
                user_id = user["user_id"]
                break
        return user_id

    def select_data_layer(self, data_layer_name):
        data_layers = self.data_layer.list_layers(project_id=self.project.id)
        for data_layer in data_layers:
            if data_layer["label"] == data_layer_name:
                data_layer_id = data_layer["id"]
                break
        self.data_layer.id = data_layer_id
        return data_layer_id

    def get_access_token(self, path, url):
        full_path = os.path.join(os.getcwd(), path, "user_pass.json")
        with open(full_path, "r") as file:
            data = json.load(file)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer <JWT>",
        }
        tokens = response_json(requests.post)(url=f"{url}/api/auth/tokens", data=json.dumps(data), headers=headers)
        return tokens["access_token"]


obj = DataMaker()

