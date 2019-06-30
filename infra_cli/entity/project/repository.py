from __future__ import unicode_literals
import os
import os.path

import yaml
from semver import VersionInfo

from infra_cli.schema import validate_project
from .models import Project

MANIFEST_DIR = os.environ.get("INFRA_MANIFEST_DIR", ".infra")
PROJECT_MANIFEST_FILE = os.environ.get("INFRA_PROJECT_MANIFEST", "project.yaml")

KEY_ROOT = "project"
KEY_PROJECT_NAME = "name"
KEY_PROJECT_VERSION = "version"
KEY_PROJECT_REPOSITORY = "repository"


def _version_representer(dumper, data):
    return dumper.represent_data(str(data))


def _project_representer(dumper, data):
    value = {
        KEY_PROJECT_NAME: data.name,
        KEY_PROJECT_VERSION: data.version,
    }

    if data.repository:
        value[KEY_PROJECT_REPOSITORY] = data.repository

    return dumper.represent_mapping(u'tag:yaml.org,2002:map', [(KEY_ROOT, value)])


def _read_project_file(manifest_file):
    try:
        if os.path.exists(manifest_file):
            return yaml.safe_load(open(manifest_file, "r"))
    except Exception as e:
        pass

    return {}


def _read_project(manifest_file):
    document = _read_project_file(manifest_file)

    validate_project(manifest_file, document)

    project = document.get("project", {})

    project.setdefault('team', [])
    project.setdefault('version', '0.0.0')

    return project['name'], project['version'], project['team']


def get_project(directory):
    manifest_file = os.path.join(directory, MANIFEST_DIR, PROJECT_MANIFEST_FILE)

    if not os.path.isfile(manifest_file):
        raise ValueError("No project at %s" % directory)

    name, version, teams = _read_project(manifest_file)

    return Project(directory, name, version, teams)


def find_projects(directory):
    for root, dirs, files in os.walk(directory):
        if root.startswith(os.path.join(directory, "/venv")):
            continue

        if "/." in root:
            continue

        if MANIFEST_DIR not in dirs:
            continue

        try:
            yield get_project(root)
        except ValueError:
            pass


def save_project(project):
    manifest_file = os.path.join(project.directory, MANIFEST_DIR, PROJECT_MANIFEST_FILE)

    if not os.path.isdir(project.directory):
        raise ValueError("Project root %s is not a directory")

    if not os.path.isdir(os.path.dirname(manifest_file)):
        os.mkdir(os.path.dirname(manifest_file))

    yaml.add_representer(VersionInfo, _version_representer, Dumper=yaml.SafeDumper)
    yaml.add_representer(Project, _project_representer, Dumper=yaml.SafeDumper)

    # Maybe this should be a temporary file but fo rnow I think this is reasonable..
    if os.path.isfile(manifest_file):
        with open(manifest_file, 'r') as manifest_handle:
            previous_value = manifest_handle.read()

    try:
        return yaml.safe_dump(project, open(manifest_file, 'w+'))
    except Exception:
        if previous_value is None:
            if os.path.isfile(manifest_file):
                os.unlink(manifest_file)
        else:
            with open(manifest_file, 'r') as manifest_handle:
                needs_revert = previous_value != manifest_handle.read()

            if needs_revert:
                with open(manifest_file, 'w') as manifest_handle:
                    manifest_handle.write(previous_value)
        raise
