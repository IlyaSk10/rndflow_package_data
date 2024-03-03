class Node(object):

    def __init__(self, server, project_id=None):
        self.server = server
        self.project_id = project_id or self.project_id
        self.id = None

    def list_node_files(self, node_id, project_id=None):
        print(f"Node files receiving from #{node_id} node #{self.project_id} project ...\n", end="")
        self.all_files = self.server.get(endpoint=f"/projects/{self.project_id}/nodes/{node_id}/files")
        return self.all_files

    def list_nodes(self, project_id):
        self.project_id = project_id or self.project_id
        print(f"Nodes list from #{self.project_id} project receiving ...\n", end="")
        self.all = self.server.get(endpoint=f"/projects/{self.project_id}/nodes")
        return self.all

    def read(self, project_id=None, node_id=None):
        self.project_id = project_id or self.project_id
        self.id = node_id or self.id
        print(f"Reading #{self.id} node from #{self.project_id} project ...\n", end="")
        self.data = self.server.get(endpoint=f"/projects/{self.project_id}/nodes/{self.id}")
        return self.data
