#!/bin/bash

### PLEASE use 123 for ldap admin password!
set -euo pipefail

sudo apt update
sudo apt install samba smbldap-tools slapd ldap-utils -y

sudo cp --verbose --force "/etc/samba/smb.conf" "/etc/samba/smb.conf.origin"
sudo cp --verbose --force "smb.conf" "/etc/samba/smb.conf"
sudo chown root:root "/etc/samba/smb.conf"

## test.org
## dc=test,dc=org
sudo dpkg-reconfigure slapd

sudo service slapd restart
cat "/usr/share/doc/samba/examples/LDAP/samba.ldif" | sudo ldapadd -Q -Y EXTERNAL -H ldapi:///

sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f samba_indices.ldif
sudo service slapd restart

sudo service smbd restart

#sudo smbldap-config
sudp cp --verbose --force "/etc/smbldap-tools/smbldap_bind.conf" "/etc/smbldap-tools/smbldap_bind.conf.origin"
sudo cp --verbose --force "smbldap_bind.conf" "/etc/smbldap-tools/smbldap_bind.conf"
sudo chown root:root "/etc/smbldap-tools/smbldap_bind.conf"
sudo chmod 600 "/etc/smbldap-tools/smbldap_bind.conf"

sudo slapcat -l backup.ldif
sudo smbldap-populate -g 10000 -u 10000 -r 10000

sudo smbpasswd -w 123
sudo service smbd restart
sudo service nmbd restart

sudo apt install libnss-ldapd libpam-ldapd -y
## IMPORTANT
## libnss-ldapd configuration:
## check passwd, shadow and group


sudo service smbd restart
sudo service nmbd restart
sudo service nscd restart
sudo service nslcd restart

# create the user group
sudo smbldap-groupadd -a usertest

# -c comment
# -a create samba and unix account
# -P invoke smbldap-passwd
# -m create home directory
# -g add primary group
# -G add secondary groups
sudo smbldap-useradd -c "usertest comment" -a -P -m -g usertest -G "Domain Users" usertest

## DEPRECIATED
## creating an unix user, presents in /etc/passwd and /etc/shadow is DEPRECIATED
## since libnss-ldapd and libpam-ldapd handle manage user via the LDAP server
## use `getent passwd`
#sudo useradd --create-home --home=/home/usertest --user-group --comment=usertest usertest