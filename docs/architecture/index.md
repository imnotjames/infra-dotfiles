# Architecture
`infra` was inspired by [the QCon AirBNB slides][qcon-airbnb] among a wide
variety of other similar approaches taken by other companies.

The Architecture documentation is intended to clarify the decisions made when
designing this deployment mechanism and answer common questions about the
objectives of `infra`.

## Goals
`infra` was designed to accomplish the following goals:

* **Deploys should be simple.**
  Deploying code should not require meditation under a waterfall, confusing
  incantations, and a complete knowledge of the cosmos.
  A beginner should be able to deploy with minimal coaching.
* **Deploys should be repeatable.**
  If a deploy can't be easily repeatable, what's the point?  Applications are
  iterated on and need to be deployed frequently and to multiple environments.
  Deploying for the eighth time should get you the same result as the first.
* **Deploys should be readable.**
  It should not take more than a few minutes to understand what it is we're
  trying to accomplish.  Abstraction can often help with this.
  Programs are meant to be read by humans and only incidentally for computers
  to execute.

Most of all, `infra` should make your life _easier_.

## Glossary
`infra` uses a few terms as shorthand for complex concepts.

Term        | Description
----------- | -------------------
Project     | Base unit in `infra` at the organization level.
Application | A working unit of a Project at the deployment level.
Environment | A separate deployment of an application.
Stack       | A basis which to make assumptions for deploying an application.
Add-Ons     | A Resource, credential, or connection which an application may use.
Pipeline    | A set of tasks to test, build, and deploy applications.
Jobs        | A task in a pipeline.
Stages      | A set of tasks in a pipeline that may run in parallel.



[qcon-airbnb]: https://qconlondon.com/system/files/presentation-slides/qcon_london_2019.pdf
