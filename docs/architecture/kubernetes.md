# Kubernetes and Infra

To enable deployment of the project on kubernetes, we utilize helm charts to handle the pipelines and deployment.  These are charts that live elsewhere (usually) and are bound together via a generated helm charts per environment.

## Environments

## Secrets

## Access Controls

## Charts

### Environment

The environment merges together parameter sets and uses dependencies to include stacks and add-ons.

### Pipeline

The pipeline runs in its own environment where it builds everything as needed and injects them into the stack container for deployment. 

### Stack

Uses ....

## Add-ons

Add-ons are sidecars or operators - inject environment variables into the stack deployment.