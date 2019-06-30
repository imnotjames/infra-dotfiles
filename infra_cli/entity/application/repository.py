from __future__ import unicode_literals

import os
import os.path

import yaml

from infra_cli.schema import validate_application
from .models import Addon, Stack, Environment, ParameterBag, Application


DEFAULT_ENVIRONMENTS = {"production", "canary", "development"}
DEFAULT_STACK_TYPE = os.environ.get("DEFAULT_STACK_TYPE", "generic")

APPLICATION_MANIFEST_DIR = "application"
APPLICATION_MANIFEST_EXTENSION = "yaml"


def _massage_stack(stack):
    if isinstance(stack, str):
        stack_project = None
        stack_type = stack
    else:
        stack_project = stack.get("project", None)
        stack_type = stack.get("type", None)

    if "@" in stack_type:
        stack_type, stack_version = stack_type.split("@", 1)
    else:
        stack_version = None

    return Stack(stack_type, stack_version, stack_project)


def _massage_addon(addon):
    if isinstance(addon, str):
        addon_project = None
        addon_type = addon
        addon_alias = None
        addon_parameters = None
    else:
        addon_project = addon.get("project", None)
        addon_type = addon.get("type")
        addon_alias = addon.get("alias", None)
        addon_parameters = addon.get("parameters", None)

    if "@" in addon_type:
        addon_type, addon_version = addon_type.split("@", 1)
    else:
        addon_version = None

    return Addon(addon_type, addon_version, addon_project, addon_alias, ParameterBag.from_dict(addon_parameters))


def _massage_parameters(parameters):
    return ParameterBag.from_dict(parameters)


def _massage_environment(name, environment, application):
    # TODO: Handle addons edge case - they're a list but matching "as" keys
    # should count as the same element in the list.
    # TODO: We can make a few assumptions about this data instead
    # of just merging it like this - we only need to do this for `options`
    # in addons and `parameters`.

    def _merge(destination, source):
        for k, v in source.items():
            if k in destination:
                if isinstance(destination[k], dict):
                    if isinstance(v, dict):
                        _merge(destination[k], v)
                    continue

                if isinstance(destination[k], list):
                    if isinstance(v, list):
                        destination[k].extend(v)
                    else:
                        destination[k].append(v)
                    continue

            destination[k] = v

    stack = _massage_stack(application.get('stack'))

    application_addons = [_massage_addon(a) for a in application.get('addons', [])]
    environment_addons = [_massage_addon(a) for a in environment.get('addons', [])]

    addons = {}
    addons.update({a.alias: a for a in application_addons})
    addons.update({a.alias: a for a in environment_addons})

    parameters = {}

    _merge(parameters, application.get('parameters', {}))
    _merge(parameters, environment.get('parameters', {}))

    parameters = _massage_parameters(parameters)

    return Environment(name, stack, tuple(addons.values()), parameters)


def _get_manifest_file(project, name):
    app_file = "%s.%s" % (name, APPLICATION_MANIFEST_EXTENSION)
    return project.get_manifest_path(APPLICATION_MANIFEST_DIR, app_file)


def _read_application_file(manifest_file):
    try:
        if os.path.exists(manifest_file):
            return yaml.safe_load(open(manifest_file, "r"))
    except:
        pass

    return {}


def _read_application(manifest_file):
    document = _read_application_file(manifest_file)

    validate_application(manifest_file, document)

    raw_application = document.get("application", {})

    if 'environments' in raw_application:
        environment_names = list(raw_application.get('environments').keys())
    else:
        environment_names = DEFAULT_ENVIRONMENTS

    stack = _massage_stack(raw_application.get('stack'))
    environments = {}

    for name in environment_names:
        environment = raw_application["environments"].get(name, {})
        environments[name] = _massage_environment(name, environment, raw_application)

    return stack, environments


def find_applications(project):
    applications_dir = project.get_manifest_path("application")

    if not os.path.isdir(applications_dir):
        return []

    for d in os.listdir(applications_dir):
        name, ext = os.path.splitext(d)

        # Skip applications that start with "." in the name
        if name.startswith("."):
            continue

        # Only applications with an extension of YAML
        if ext != ".%s" % APPLICATION_MANIFEST_EXTENSION:
            continue

        yield get_application(project, name)


def get_application(project, name):
    manifest_file = _get_manifest_file(project, name)

    stack, environments = _read_application(manifest_file)

    yield Application(project, name, stack, environments)
