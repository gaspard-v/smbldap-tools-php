#!/usr/bin/env bash

set -euxo pipefail

LDAP_PREFIX="${LDAPPREFIX:-"dc=test,dc=org"}"

install_dependencies() {
    apt update
    apt install --yes \
        samba \
        smbldap-tools \
        slapd ldap-utils \
        libnss-ldapd \
        libpam-ldapd
}

write_samba_config() {
    local admin_dn="cn=admin,$LDAP_PREFIX"
}

install_dependencies
cp --verbose --force "/etc/samba/smb.conf" "/etc/samba/smb.conf.origin"


cat << EOF


    ##### LDAP ######
    passdb backend = ldapsam:ldap://127.0.0.1
    ldap suffix = dc=test,dc=org
    ldap machine suffix = ou=Machine
    ldap user suffix = ou=User
    ldap group suffix = ou=Group
    ldap admin dn = cn=admin,dc=test,dc=org
    ldap ssl = off
    ldap passwd sync = Yes


EOF
