import json
import os

from jsonschema import Draft7Validator

PROJECT_SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "..", "schema/project.json")
PROJECT_SCHEMA = json.load(open(PROJECT_SCHEMA_FILE))

APPLICATION_SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "..", "schema/application.json")
APPLICATION_SCHEMA = json.load(open(APPLICATION_SCHEMA_FILE))

PIPELINE_SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "..", "schema/pipeline.json")
PIPELINE_SCHEMA = json.load(open(PIPELINE_SCHEMA_FILE))


class ValidationError(Exception):
    def __init__(self, identifier, errors):
        super(ValidationError, self).__init__("%s failed validation: %s" % (identifier, "; ".join(str(e) for e in errors)))

        self.identifier = identifier
        self.__errors = tuple(errors)

    @property
    def errors(self):
        return self.__errors


def validate_project(identifier, document):
    validator = Draft7Validator(PROJECT_SCHEMA)

    errors = sorted(validator.iter_errors(document), key=lambda e: e.path)

    if errors:
        raise ValidationError(identifier, errors)


def validate_application(identifier, document):
    validator = Draft7Validator(APPLICATION_SCHEMA)

    errors = sorted(validator.iter_errors(document), key=lambda e: e.path)

    if errors:
        raise ValidationError(identifier, errors)


def validate_pipeline(identifier, document):
    validator = Draft7Validator(PIPELINE_SCHEMA)

    errors = sorted(validator.iter_errors(document), key=lambda e: e.path)

    if errors:
        raise ValidationError(identifier, errors)
