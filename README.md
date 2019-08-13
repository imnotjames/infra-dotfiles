# Project Infra Dotfiles
## Giving Everyone the Heroku Experience

`infra` is an opinionated set of schemas and command-line tools to describe and manage
your applications as configuration.  Define a project, applications, and pipelines -
then let infra take care of the rest.

Use `infra` to

* Deploy your latest and greatest application to kubernetes clusters
* Provision third party resources as part of a deploy, such as databases,
  monitoring tools, and more
* Manage a platform-agnostic CI/CD pipeline
* Define ownership across a repository
* Record metadata that is the glue between your team and your application

See the documentation to learn more about the concepts and configurations available.

## Installation

See the [installation guide](./docs/installation/) for more information.

## Documentation

See the [documentation](./docs/index.md) to learn more about the manifest format,
deployment mechanisms available, and decisions behind this project.

## Acknowledgements

* Melanie Cebula for the fantastic [the QCon AirBNB slides][qcon-airbnb] that inspired this.
* GitLab CI for [their pipeline documentation][gitlab-ci-yaml] that much of the pipeline definitions are lifted from.

[qcon-airbnb]: https://qconlondon.com/system/files/presentation-slides/qcon_london_2019.pdf
[gitlab-ci-yaml]: https://docs.gitlab.com/ee/ci/yaml/