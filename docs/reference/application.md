# Application Reference
## Introduction
The Application manifest is defined within `.infra/application/`.
The name of the file will define the name of the application.

### Unavailable names for Environments
While nearly any string is available as an environment, the following may not be used.

* `environments`
* `default`

## `default` environment
Any configuration parameter for the `default` environment is applied on every other
environment defined in the application.

## Configuration Parameters

Parameter           | Description
------------------- | --------------------
`environments`      | 
`stack`             |
`stack:type`        |
`stack:project`     |
`stack:parameters`  |
`addons`            |
`addons:type`       |
`addons:project`    |
`addons:alias`      |
`addons:parameters` |
`parameters`        |

## Parameter Details

### `environments`
A list of environments, at the root of the manifest.

### `stack`
A stack may defined as a string that refers to the `type`.

#### `stack:type`

#### `stack:project`

#### `stack:parameters`

### `addons`

#### `addons:type`

#### `addons:project`

#### `addons:alias`

#### `addons:parameters`

### `parameters`

## Special YAML Features
YAML can use pointers to copy

### Hidden Environments
Environments that start with a period (`.`) are "hidden" and are not
used as an environment.  Instead, they may be used as a template for
the application.
