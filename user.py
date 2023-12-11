import getpass
import os
import json

from additional import get_from_json


class User(object):

    def __init__(self, server, json_path=None):
        self.server=server
        self.data = None
        self.json_path = json_path

    def login(self, json_path=None):
        if self.data is not None:
            print("Already logged in. Logout at first.")
            return None
        self.json_path = json_path or self.json_path
        if self.json_path is None:
            print("User pass is absent")
            return None
        user_pass = self._get_user_pass(json_path=self.json_path)
        print(f"Logging in as \"{user_pass['username']}\" ...", end="")
        response = self.server.post(endpoint="/auth", data=user_pass)
        return response

    def _get_user_pass(self, json_path=None):
        if json_path is None or not os.path.exists(json_path):
            return dict(
                username = input("Enter username: "),
                password = getpass.getpass("Enter password: ")
            )
        return get_from_json(json_path)

    def refresh(self):
        if self.data is None:
            return
        print("Refreshing authentication ...", end="")
        response = self.server.post(endpoint="/auth/refresh")
        return response

    def login_tokens(self):
        print("Login tokens receiving ...", end="")
        user_pass = self._get_user_pass(self.json_path)
        self.tokens = self.server.post(endpoint="/auth/tokens", data=user_pass)
        if self.tokens is not None:
            self.server.access_token = self.tokens["access_token"]
            self.server.refresh_token = self.tokens["refresh_token"]

    def refresh_tokens(self):
        print("Login tokens refreshing ...", end="")
        self.tokens = self.server.post(endpoint="/auth/tokens/refresh")
        return self.tokens

    def logout(self):
        if self.data is None:
            return
        print("Logging out ...", end="")
        response = self.server.post(endpoint="/auth/logout")
        self.server.token = "<JWT>"
        return response

    def list_users(self):
        print(f"Listing all users ...", end="")
        self.all = self.server.get(endpoint="/users")
        return self.all

