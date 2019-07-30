# Pipeline
A pipeline is a set of actions a project should take to test, build, and deploy the
applications. A project may have multiple pipelines - some which may not directly map
up to a specific application.  Each pipeline can have stages defined, and each stage may
have multiple jobs to perform.

For more detailed information about the pipeline configuration, see
[the Pipeline reference pages](../reference/pipeline.md).

## Jobs
A job is a part of a pipeline.

## Scripts

## Stages
A stage is a part of the pipeline.  When a job belongs to a stage it may run
in parallel to other jobs within that stage.

## Services
A service is a part of a job.  A service
