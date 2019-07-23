# Infra Glossary

### Project

A project traditionally is defined at the root of a repository under the folder
`.infra` using a project.yml manifest. The project manifest requires a name.
Optionally, you may define version, ownership details, or contact information.

A pipeline is a set of actions a project should take to test, build, and deploy the
applications. A project may have multiple pipelines - some which may not directly map
up to a specific application.  Each pipeline can have stages defined, and each stage may
have multiple jobs to perform.

For more detailed information about the project configuration, see
[the Project pages](./docs/project/).

### Application

An application is a unit of a project. A project may have multiple applications. An
application is defined as an environment, a stack, and add-ons.

For more detailed information about the application configuration, see
[the Application pages](./docs/application/).

#### Environment

Production, Canary, Staging, Development. 

#### Stack

The stack is a required part of the application.  The stack defines a basis which to make
assumptions from on deploying your application.  The stack utilizes the application's
parameters to configure itself.

Examples of stacks may be a Django web application, a generic command line cron task, or
a Java Storm topology.

The stack may imply a number of other pipelines or add-ons to be enabled as part of it by
default.  This is dependent on the creator of the stack, the needs of the environment,
toolchain build steps, or the frameworks involved.

#### Add-Ons

An add-on is an optional part of the application.  Add-ons are resources, credentials, or
connections which an application may use.  In most cases, the add-ons are injected as
environment variables into the stack.  An add-on uses the add-on's parameters to configure
itself.

Examples of add-ons may be Amazon Web Services managed databases, Redis instances provisioned
as a cache, access tokens for Sentry error tracking, or connection parameters for on-premise
logging infrastructure.

An add-on may imply a number of other pipelines or add-ons as part of it by default.  This is
dependent on the creator of the add-on, the needs of the environment,
toolchain build steps, or the frameworks involved.

### Pipeline

For more detailed information about the pipeline configuration, see 
[the Pipeline pages](./docs/pipeline/).

#### Stages

#### Jobs

#### Services