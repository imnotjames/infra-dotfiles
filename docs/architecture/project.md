### Project
A project traditionally is defined at the root of a repository under the folder
`.infra` using a project.yml manifest. The project manifest requires a name.
Optionally, you may define version, ownership details, or contact information.

A pipeline is a set of actions a project should take to test, build, and deploy the
applications. A project may have multiple pipelines - some which may not directly map
up to a specific application.  Each pipeline can have stages defined, and each stage may
have multiple jobs to perform.

For more detailed information about the project configuration, see
[the Project reference pages](./reference/project.md).
