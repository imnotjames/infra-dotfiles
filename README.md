# Project Infra Dotfiles
## Giving Everyone the Heroku Experience

A dumping ground of ideas for infra configuration.

Inspired by [the QCon AirBNB slides](https://qconlondon.com/system/files/presentation-slides/qcon_london_2019.pdf)

### CLI

#### infra init

Create a new project in the current root.

This creates a project without any applications or any configuration.

#### infra apps

#### infra apps init APP

Create an application in the current root and project.

#### infra apps destroy APP

#### infra stacks

#### infra stack set STACK

#### infra stack config
 
#### infra stack config KEY

#### infra stack config KEY VALUE

#### infra stack config --unset KEY

#### infra addons

#### infra addons attach ADDON

#### infra addons detach ADDON

#### infra addons rename ADDON NEW_NAME

#### infra addons config ADDON

#### infra addons config ADDON KEY

#### infra addons config ADDON KEY VALUE

#### infra addons config ADDON --unset KEY

#### infra validate

Validate the current infrastructure configuration.

#### infra export codeowners

Export a Github-Format CODEOWNERS file.

#### infra export charts

Export Kubernetes Charts based on the stacks and addons defined in your application.

#### infra export gitlab-ci

Export a Gitlab CI pipeline for all applications and sub-projects.

#### infra deploy
 