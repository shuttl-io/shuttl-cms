# shuttl-cms

This is a great CMS. Everyone says so.

## Installation
To install (Right now this only works on mac osx, maybe linux as well) run:
`source <(curl -s https://raw.githubusercontent.com/shuttl-io/shuttl/master/install.sh)`

## Usage

run `shuttl launch` in the command line. Then go to shuttl.shuttl.local:5000 in your browser and login and use the interface

### To add a new organization:
run `shuttl add --organization [<organization name>]`

### To add a new user:
run `shuttl add --user [<user name> --organization <organization name>]`

### To make a new transport:
run `shuttl add --transport <protocol> [--website <website name>]`
*Protocol must be git or S3*