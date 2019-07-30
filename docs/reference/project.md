# Project Reference

A project traditionally is defined at the root of a repository under the folder
`.infra` using a `project.yml` manifest. The project manifest requires a name.
Optionally, you may define version, ownership details, or contact information.


## Introduction

### Restrictions on Projects

## Configuration Parameters

Parameter       | Description
--------------- | --------------------
`version`       |

### Parameter Details

#### `version`

#### `owner`

#### `contact`

#### `contact:slack`

#### `contact:email`

#### `contact:only` and `contact:except`
Substring match or regular expression match of the type of contact.

Special keywords:

Keyword       | Description
------------- | -----------------------
`support`     | General Support inquiries.
`bugs`        | Bug Reports.
`crashes`     | Crash Logs and other similar Reports
`alert:high`  | High Severity Alerts, such as "critical" thresholds.
`alert:low`   | Low Severity Alerts, such as "warning" thresholds.
`exception`   | Exceptions and Regressions, such as from Sentry.
`maintenance` | Scheduled Maintenance, such as expected downtime.
