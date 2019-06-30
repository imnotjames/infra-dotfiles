from __future__ import unicode_literals

import re
from collections import Mapping


class Addon:
    def __init__(self, addon_type, addon_version=None, addon_project=None, addon_alias=None, addon_parameters=None):
        self.__type = addon_type
        self.__version = addon_version
        self.__project = addon_project
        self.__alias = addon_alias
        self.__parameters = addon_parameters

    @property
    def type(self):
        return self.__type

    @property
    def version(self):
        return self.__version

    @property
    def project(self):
        return self.__project

    @property
    def alias(self):
        if self.__alias:
            return re.sub('[^0-9a-zA-Z]', '_', self.__alias).upper()

        return "%s_DEFAULT" % re.sub('[^0-9a-zA-Z]', '_', self.__type).upper()

    @property
    def parameters(self):
        return self.__parameters if self.__parameters else ParameterBag()


class Stack(Addon):
    def __init__(self, stack_type, stack_version=None, stack_project=None, stack_parameters=None):
        super(Stack, self).__init__(
            stack_type,
            stack_version,
            stack_project,
            "%s stack" % stack_type,
            stack_parameters
        )


class Environment:
    def __init__(self, name, stack, addons, parameters):
        self.__name = name
        self.__stack = stack
        self.__addons = tuple(addons) if addons else tuple()
        self.__parameters = parameters

    @property
    def name(self):
        return self.__name

    @property
    def stack(self):
        return self.__stack

    @property
    def addons(self):
        return self.__addons

    @property
    def parameters(self):
        return self.__parameters


class ParameterBag(Mapping):
    @staticmethod
    def __from_list(items):
        output = []
        for v in items:
            if isinstance(v, dict):
                v = ParameterBag.from_dict(v)

            if isinstance(v, (list, tuple)):
                v = ParameterBag.__from_list(v)

            output.append(v)

        return tuple(output)

    @staticmethod
    def from_dict(dictionary):
        if not dictionary:
            return ParameterBag()

        if not isinstance(dictionary, dict):
            raise TypeError()

        output = {}
        for k, v in dictionary.items():
            if isinstance(v, dict):
                v = ParameterBag.from_dict(v)

            if isinstance(v, (list, tuple)):
                v = ParameterBag.__from_list(v)

            output[k] = v

        return ParameterBag(**dictionary)

    @staticmethod
    def __unpack(values):
        if isinstance(values, (tuple, list)):
            return [ParameterBag.__unpack(v) for v in values]

        if isinstance(values, (ParameterBag, dict)):
            return {k: ParameterBag.__unpack(values[k]) for k in values}

        return values

    def as_dict(self):
        return ParameterBag.__unpack(self.__values)

    def __init__(self, **kwargs):
        self.__values = {}
        self.__values.update(kwargs)

    def __len__(self):
        return len(self.__values)

    def __iter__(self):
        return iter(self.__values)

    def __getitem__(self, k):
        return self.__values[k]

    def __contains__(self, key):
        return key in self.__values


class Application:
    def __init__(self, project, name, stack, environments):
        self.project = project
        self.name = name

        self.__stack = stack
        self.__environments = environments

    @property
    def manifest_file(self):
        return _get_manifest_file(self.project, self.name)

    @property
    def stack(self):
        return self.__stack

    @property
    def environments(self):
        return tuple(self.__environments.keys())

    def get_environment(self, name):
        return self.__environments.get(name)
