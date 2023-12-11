class Project(object):

    def __init__(self, server, project_id=None):
        self.id = project_id
        self.data = None
        self.server = server
        if self.id is not None:
            self.read()

    def list_projects(self):
        print("Projects list receiving ...", end="")
        self.all = self.server.get("/projects")
        return self.all

    def read(self, project_id=None):
        self.id = project_id or self.id
        print(f"Reading #{self.id} project ...", end="")
        self.data = self.server.get(f"/projects/{self.id}")
        return self.data

    def list_project_users(self, project_id=None):
        project_id = project_id or self.id
        print(f"Listing all users of #{project_id} project ...", end="")
        self.users = self.server.get(endpoint=f"/projects/{project_id}/users")
        return self.users
