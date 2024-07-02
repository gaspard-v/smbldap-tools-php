# SMBLDAP Tools for PHP and Python

This project aims to simulate CLI tools "smbldap-tools"
on a web interface.

This project has two mains parts:

## miniserver

Miniserver is a tiny TCP server. Its purpose is to
change LDAP user data AND/OR Linux passwd/shadow files.

## Laravel front

The web interface is build with Laravel.
The interface works like an admin panel.
User can change it's password.
It communicates with the miniserver.
