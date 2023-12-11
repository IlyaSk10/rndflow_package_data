class Parameters():
    def __init__(self, server, project_id):
        self.server = server
        self.project_id = project_id

    def list_param_values(self, node_id, data_layer_id, project_id=None):
        self.project_id = project_id or self.project_id
        print(f"Listing parameters values for #{node_id} node or #{self.project_id} project ...", end="")
        params = {"data_layer_id": data_layer_id}
        self.all_param_values = self.server.get(endpoint=f"/projects/{self.project_id}/nodes/{node_id}/param_values", params=params)
        return self.all_param_values

    def update_param_value(self, node_id, value, schema_id=None, project_id=None):
        self.project_id = project_id or self.project_id
        self.id = schema_id or self.id
        print(f"Updating #{schema_id} param value in #{node_id} or #{self.project_id} to {value} ...", end="")
        params = {"data_layer_id": data_layer_id}
        self.server.put(f"/project/{self.project_id}/nodes/{node_id}/param_values/{self.id}", data=(value), params=params)
