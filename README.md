[![Build Status](https://travis-ci.org/viasite-ansible/ansible-role-site.svg?branch=master)](https://travis-ci.org/viasite-ansible/ansible-role-site)

# ansible-role-site
Ansible role for setup php site.

Role has many dependencies to other viasite-ansible roles, so I don't think that you can easy use it.

- sites/*.yml - each yml = site

# Dependencies
- viasite-ansible.apache-vhosts (that depends to viasite-ansible.apache)
- viasite-ansible.cron
- viasite-ansible.git
- viasite-ansible.mysql
- viasite-ansible.nginx
- viasite-ansible.ssh-keys
- viasite-ansible.vim
- viasite-ansible.zsh

# TODO:
- site with main www domain
- SSL, letsencrypt
- add site to hosts_sites
- disable, rename and delete site
- DNS
- apache: PHP select
- DKIM
- tests



# Setup new site
1. Copy sites/_site_template.yml to sites/`site_user`.yml
2. Add role to sites.yml: ```- { role: site, site_vars_file: sites/site_user.yml }```
3. Exec playbook: ```ansible-playbook sites.yml -v```


## Example playbook
