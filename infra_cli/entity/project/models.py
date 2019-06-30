from __future__ import unicode_literals
import os
import os.path


MANIFEST_DIR = os.environ.get("INFRA_MANIFEST_DIR", ".infra")


class Team:
    def __init__(self, name, github_team=None):
        self.__name = name
        self.__github_team = github_team if github_team else name

    @property
    def name(self):
        return self.__name

    def github_team(self):
        return self.__github_team


class Contact:
    pass


class Repository:
    pass


class Project:
    def __init__(self, directory, name, version=None, repository=None, teams=tuple()):
        self.directory = directory
        self.name = name
        self.version = version
        self.__teams = teams
        self.repository = repository

    @property
    def teams(self):
        return "@hello",

    @property
    def manifest_directory(self):
        return os.path.join(self.directory, MANIFEST_DIR)

    def get_manifest_path(self, *paths):
        return os.path.join(self.manifest_directory, *paths)
