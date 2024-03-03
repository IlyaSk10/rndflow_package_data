import os


class Package(object):
    def __init__(self, server, project_id=None, node_id=None, data_layer_id=None):
        self.site = server
        self.project_id = project_id
        self.id = None
        self.node_id = node_id
        self.data_layer_id = data_layer_id

    def search(self, data=None, project_id=None, node_id=None, master_id=None, data_layer_id=None):
        self.project_id = project_id or self.project_id
        self.node_id = node_id or self.node_id
        self.data_layer_id = data_layer_id or self.data_layer_id
        if self.data_layer_id is None:
            return None
        print(f"Searching packages in #{self.node_id} node of #{self.project_id} project ...\n", end="")
        data = data or {
            "master_id": master_id or 0,
            "sort_by": "id",
            "descending": True,
            "field_filter_name": "",
            "field_filter_op": "",
            "field_filter_value": "",
            "jobs_filter_op": "",
            "jobs_filter_count_value": 0,
        }
        params = {
            "data_layer_id": self.data_layer_id,
        }
        self.all = self.site.post(endpoint=f"/projects/{self.project_id}/nodes/{self.node_id}/packages/search",
                                  data=data, params=params)
        return self.all

    def read(self, node_id, package_id):
        self.project_id = project_id or self.project_id
        self.node_id = node_id or self.node_id
        self.id = package_id or self.id
        if None in (self.project_id, self.node_id, self.id):
            return None
        print(f"Reading data from #{self.id} package #{self.node_id} node of #{self.project_id} project", end="")
        self.data = self.site.get(endpoint=f"/projects/{self.project_id}/nodes/{self.node}/packages/{self.package_id}")
        return self.data

    def download(self, save_path, project_id=None, node_id=None, package_ids=None, data_layer_id=None):
        self.project_id = project_id or self.project_id
        self.node_id = node_id or self.node_id
        self.data_layer_id = data_layer_id or self.data_layer_id
        if self.data_layer_id is None:
            return None
        if None in (self.project_id, self.node_id):
            return None
        params = {
            "data_layer_id": self.data_layer_id
        }
        if package_ids is None or len(package_ids) == 0:
            return
        for package_id in package_ids:
            file_path = os.path.join(save_path, f"{str(package_id)}.tar")
            print(
                f"Downloading #{package_id} package #{self.node_id} node of #{self.project_id} project to: {file_path}... \n",
                end="")
            data = {
                "packages": [package_id, ],
            }
            response = self.site.post(endpoint=f"/projects/{self.project_id}/nodes/{self.node_id}/packages/download",
                                      data=data, params=params)
            with open(file_path, 'wb') as f:
                f.write(response)
            print(f"File downloaded and saved to: {file_path} \n")
