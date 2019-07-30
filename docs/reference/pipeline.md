# Pipeline Reference

## Introduction

## Validate the Pipeline YAML

## Unavailable names for Jobs

* `image`
* `services`
* `stages`
* `before_script`,
* `after_script`
* `variables`
* `cache`

## Configuration Parameters

A job a list of parameters that define the job's behavior.

Parameter                                          | Description
-------------------------------------------------- | --------------------
[`script`](#script)                                | Defines a set of commands that are executed as the job.
[`before_script`](#before_script-and-after_script) | Defines a set of commands that are executed before the job.
[`after_script`](#before_script-and-after_script)  | Defines a set of commands that are executed after the job.
[`image`](#image)                                  | Defines a docker image.
[`services`](#services)                            | Defines docker service images.
[`stage`](#stage)                                  | Defines a job to be part of a stage.
[`only`](#only)                                    | Prevent a job from running when it doesn't match.
[`except`](#except)                                | Prevent a job from running when it does match.
[`tags`](#tags)                                    | Defines tags to limit where this job may run.
[`allow_failure`](#allow_failure)                  | Permit a job to fail without affecting the pipeline.
[`when`](#when)                                    | Defines when to run the job.
[`cache`](#cache)                                  | Defines a set of files that should be cached between job runs.
[`artifacts`](#artifacts)                          | Defines a set of files that should be saved on success.
[`dependencies`](#dependencies)                    | Defines a set of other jobs that this job depends on so artifacts may be passed between.
[`retry`](#retry)                                  | Defines when and how many times a job may be retried when failing.
[`parallel`](#parallel)                            | Defines how many instances of a job may be run in parallel.
[`variables`](#variables)                          | Defines job variables.

### Setting Default Parameters

### Parameter Details

#### `script`
`script` is a shell script which is executed by the runner of the pipeline.

`script` may be a string:
```yaml
job:
  script: make
```
or a list of strings:
```yaml
job:
  script:
    - make
    - ./a.out
```

#### `before_script` and `after_script`

#### `image`

#### `image:name`

#### `image:entrypoint`

#### `services`

##### `services:name`

##### `services:alias`

##### `services:entrypoint`

##### `services:command`

#### `stages` and `stage`

#### `only` and `except`

#### `tags`

#### `allow_failure`

#### `when`

#### `cache`

#### `artifacts`

#### `dependencies`

#### `retry`

#### `parallel`

#### `variables`

## Useful features

### Special YAML Features
YAML anchors, aliases, and mapp merging.

### Using Reserved Keywords
Want to use `true` or `false`? Wrap it in a quote.

### Hidden Jobs
A job may be hidden by prepending its name with a dot (`.`).  Hidden jobs
are not executed by the pipeline, but are still parsed as YAML.

For example:

```yaml
.hidden_job: &job_template
  before_script: make
```

### Using Anchors
```yaml
.hidden_job: &job_template
  image: gcc:latest
  script: make

test:
    <<: *job_template
```

```yaml
.hidden_job: &job_template
  image: gcc:latest
  script: make test

.postgres_services:
  services: &postgres_services_template
    - postgres
    - proxysql
    - redis

.mysql_services:
  services: &mysql_services_template
    - mysql
    - proxysql
    - redis

test_postgres:
    <<: *job_template
    services: *postgres_services_template

test_mysql:
    <<: *job_template
    services: *mysql_services_template
```
