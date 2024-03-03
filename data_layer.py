class DataLayer():
    def __init__(self, server, project_id=None, data_layer_id=None):
        self.id = data_layer_id
        self.server = server
        self.project_id = project_id

    def list_layers(self, project_id=None):
        self.project_id = project_id or self.project_id
        print(f"Listing data layers for #{self.project_id} project ...\n", end="")
        self.all = self.server.get(endpoint=f"/projects/{self.project_id}/data_layers")
        return self.all

    def create(self, project_id=None, data=None):
        self.project_id = project_id or self.project_id
        print(f"Data layers creation for #{self.project_id} project ...", end="")
        data = data or {
            "layer": input("Layer: "),
            "description": input("Description: "),
        }
        self.data = self.server.post(endpoint=f"/projects/{self.project_id}/data_layers", data=data)
        self.id = self.data["id"]
        return self.data

    def last(self, project_id=None):
        self.project_id = project_id or self.project_id
        print(f"Getting last data layer for #{self.project_id} project ...", end="")
        self.data = self.server.get(endpoint=f"/projects/{self.project_id}/data_layers/last")
        self.id = self.data["id"]
        return self.data

    def read(self, project_id=None, data_layer_id=None):
        self.id = data_layer_id or self.id
        self.project_id = project_id or self.project_id
        print(f"Reading #{self.id} data layer for #{self.project_id} project ...", end="")
        self.data = self.server.get(endpoint=f"/projects/{self.project_id}/data_layers/{self.id}")
        self.id = self.data["id"]
        return self.data

    def update(self, project_id=None, data_layer_id=None, data=None):
        self.id = data_layer_id or self.id
        self.project_id = project_id or self.project_id
        print(f"Updating #{self.id} data layer for #{self.project_id} project ...", end="")
        data= data or {
            "label": input("Label: "),
            "description": input("Description: "),
            "is_active": True,
            "is_personal": True,
        }
        self.data = self.server.get(endpoint=f"/projects/{self.project_id}/data_layers/{self.id}", data=data)
        self.id = self.data["id"]
        return self.data

    def delete(self, project_id, data_layer_id):
        self.id = data_layer_id or self.id
        self.project_id = project_id or self.project_id
        print(f"Deleting #{self.id} data layer for #{self.project_id} project ...", end="")
        response = self.server.delete(endpoint=f"/projects/{self.project_id}/data_layers/{self.id}")
        return response
