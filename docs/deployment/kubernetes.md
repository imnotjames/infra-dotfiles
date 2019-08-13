# Kubernetes and Infra

To enable deployment of a Project on kubernetes, we utilize helm charts to handle
the pipelines and deployment.

Each application and environment is translated into a generated `helm` chart and
dependency graph so that it may pull in the needed dependencies to accomplish its
needs.

## Environments

## Secrets

## Access Controls

## Charts

### Environment

The environment merges together parameter sets and uses dependencies to include stacks
and add-ons.

### Pipeline

The pipeline runs in its own environment where it builds everything as needed and
injects them into the stack container for deployment. 

### Stack
A stack translates to a specific Kubernetes deployment.

## Add-ons
Add-ons are defined as deployments, sidecars, or operators.  These dependd on
how the add-on needs to operate.  The add-ons also inject information into the stack
as an environment variable.

For example, an RDS Aurora MySQL add-on would utilize the AWS Kubernetes Operators to
generate the database - while updating a `ConfigMap` and `Secret` so that the `Stack`
deployment may pull it into the application.

The `add-on` project repository should have a `chart` directory under the path to the add-on which
