class Apikey(object):
    def __init__(self, server, project_id):
        self.project_id = project_id
        self.template_id = None
        self.server = server
        self.data= None

    def list_apikeys(self, project_id):
        print("Apikeys list receiving ...")
        self.all = self.server.get(endpoint=f"/projects/{project_id}/apikeys/templates")
        return self.all

    def create(self, project_id=None, data=None):
        if data is None:
            return None
        self.project_id = project_id or self.project_id
        print(f"Creating an apikey for #{self.project_id} project ...")
        self.data = self.server.post(endpoint=f"/projects/{self.project_id}/apikeys/templates", data=data)
        return self.data

    def update(self, project_id=None, template_id=None, data=None):
        if data is None:
            return None
        self.project_id = project_id or self.project_id
        self.template_id = template_id or self.template_id
        print(f"Updating the #{self.template_id} apikey template for #{self.project_id} project ...")
        self.data = self.server.put(endpoint=f"/projects/{self.project_id}/apikeys/templates/{self.template_id}", data=data)
        return self.data

    def request(self, project_id=None, template_id=None):
        self.project_id = project_id or self.project_id
        self.template_id = template_id or self.template_id
        print(f"Requesting the #{self.template_id} apikey template for #{self.project_id} project ...")
        self.data = self.server.post(endpoint=f"/projects/{self.project_id}/apikeys/available/{self.template_id}/request", data={})
        return self.data

    def revoke(self, apikey_id, project_id=None):
        self.project_id = project_id or self.project_id
        print(f"Revoking the #{apikey_id} apikey for #{self.project_id} project ...")
        revoke_msg = self.server.delete(endpoint=f"/projects/{self.project_id}/apikeys/{apikey_id}", data={})
        return revoke_msg
