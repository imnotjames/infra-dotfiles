# Application
An application is a unit of a project. A project may have multiple applications.
An application is defined as an Environment, a Stack, and Add-ons.

For more detailed information about the application configuration, see
[the Application reference pages](../reference/application.md).

## Environment
An environment is a part of the Application.  Each defined environment is a
separate deployment of the application.  The environments can be thought of
as a namespace within the application.

Per-environment configuration of the Stack and Add-ons is allowed. For example,
a Development environment may have debug logs enabled, where a Production
environment would perform poorly with debug logs being emitted.

While it's possible to provision resources to be shared between environments
this is generally a discouraged practice.  This is dependent on support within
the Stack and Add-On.

The default environments are Production, Canary, Staging, and Development.

## Stack
The stack is a required part of the application.  The stack defines a basis
which to make assumptions from on deploying your application.  The stack has a
type, version, and project.  The stack utilizes the application's parameters
to configure itself.

The stack may imply a number of other pipelines or Add-ons to be enabled as
part of it by default.  This is dependent on the creator of the stack, the
needs of the environment, toolchain build steps, or the frameworks involved.

Examples of stacks may be a Django web application, a generic command line
cron task, or a Java Storm topology.

## Add-Ons
An Add-on is an optional part of the application.  Add-ons are resources,
credentials, or connections which an application may use.  In most cases, the
Add-ons are injected as environment variables into the stack.  An Add-on uses
the Add-on's parameters to configure itself.

An Add-on may imply a number of other pipelines or Add-ons as part of it by
default.  This is dependent on the creator of the Add-on, the needs of the
environment, toolchain build steps, or the frameworks involved.

Examples of Add-ons may be Amazon Web Services managed databases, Redis
instances provisioned as a cache, access tokens for Sentry error tracking,
or connection parameters for on-premise logging infrastructure.
