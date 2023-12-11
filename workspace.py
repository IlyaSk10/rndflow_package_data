class Workspace(object):
    def __init__(self, server, workspace_id=None):
        self.id = workspace_id
        self.server = server
        self.data = None
        self.all_projects = None
        self.all = None
        if self.id is not None:
            self.read()

    def list_workspaces(self):
        print("Getting all workspaces list...", end="")
        self.all = self.server.get(endpoint="/workspaces")
        return self.all

    def create(self, label, description=None):
        print(f"\"{label}\" workspace creation ...", end="")
        data = dict(
           label=label,
           description=description or '',
        )
        self.data = self.server.post(endpoint="/workspaces", data=data)
        return self.data

    def read(self, workspace_id=None):
        print(f"#{workspace_id} workspace reading ...", end="")
        self.id = workspace_id or self.id
        self.data = self.server.get(endpoint=f"/workspaces/{self.id}")
        return self.data

    def list_projects(self, workspace_id=None):
        self.id = workspace_id or self.id
        print(f"#{self.id} workspace projects list receiving ...", end="")
        self.all_projects = self.server.get(endpoint=f"/workspaces/{self.id}/projects")
        return self.all_projects

