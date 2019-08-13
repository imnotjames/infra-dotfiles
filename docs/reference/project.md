# Project Reference

A project traditionally is defined at the root of a repository under the folder
`.infra` using a `project.yml` manifest. The project manifest requires a name.
Optionally, you may define version, ownership details, or contact information.


## Introduction

### Restrictions on Project Names
The project name must be at least 3 characters long.  The project name may include any
character but keep in mind that non-alphanumeric characters may be replaced with suitable
alternatives, such as with [Punycode](https://en.wikipedia.org/wiki/Punycode).

## Configuration Parameters

Parameter                                          | Description
-------------------------------------------------- | --------------------
[`version`](#version)                              |
[`owner`](#owner)                                  |
[`contact`](#contact)                              |
[`contact:slack`](#contactslack)                   |
[`contact:email`](#contactemail)                   |
[`contact:only`](#contactonly_and_contactexcept)   |
[`contact:except`](#contactonly_and_contactexcept) |

### Parameter Details

#### `version`

#### `owner`

#### `contact`
The `contact` key is set to hint to manual or automated notifications why and how to
best contact the owners of the project.

##### `contact:slack`
A slack user handle, user ID, group handle, group ID, channel handle, or channel ID.

For an internal application, the recipient is enough information to send notifications
or to allow linking to for a user to get in touch.

For external cases, however, you may need to specify the `team` or `domain` as well as
a `recipient` key for the slack communication channel.

Examples:

```yaml
contact:
- slack: U1234ABCD     # User ID
- slack: "@cooluser"   # User Handle
- slack: S1234ABCD     # Group ID
- slack: "@coolgroup"  # Group Handle
- slack: C1234ABCD     # Channel ID
- slack: "#my-project" # Channel Handle
- slack:
    team: T12345       # Explicit team to communicate with
    recipient: "#my-project"
- slack:
    domain: example     # Explicit team domain to communicate with
    recipient: "@cooluser"
```

##### `contact:email`
The email address to send a notification to.  The address is assumed to be a valid email
address.

##### `contact:only` and `contact:except`
Substring match or regular expression match of the type of contact.  May be a string
or a list of many strings.

Special keywords:

Keyword       | Description
------------- | -----------------------
`support`     | General Support inquiries.
`issues`      | Report of a bug or other problem with the project.
`security`    | Report of a possible security vulnerability or similar issue.
`crashes`     | Crash Logs and other similar Reports
`deploy`      | The start, success, or failure of each deploy.
`alert:high`  | High Severity Alerts, such as "critical" thresholds.
`alert:low`   | Low Severity Alerts, such as "warning" thresholds.
`exception`   | Exceptions and Regressions, such as from Sentry.
`maintenance` | Scheduled Maintenance, such as expected downtime.

These may be mixed and matches as needed to describe the rules of contact, as seen below:

```yaml
contact:
- slack: "#my-project-incidents"
  only:
  - crashes
  - alert:high
  - deploy
- slack: "#my-project-stakeholders"
  only:
  - maintenance
  - deploy
- email: support@my-project.com
  only: support
  except: "/Security (Issue|Report|Problem)/"
```