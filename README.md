[![Build Status](https://travis-ci.org/viasite-ansible/ansible-role-site.svg?branch=master)](https://travis-ci.org/viasite-ansible/ansible-role-site)

# ansible-role-site
Ansible role for setup php site.

- sites/*.yml - each yml = site

# Dependencies
- viasite-ansible.apache
- viasite-ansible.cron
- viasite-ansible.git
- viasite-ansible.nginx
- viasite-ansible.ssh-keys
- viasite-ansible.vim
- viasite-ansible.zsh

# TODO:
- add site to hosts_sites
- letsencrypt
- https://www.digitalocean.com/community/tutorials/how-to-host-multiple-websites-securely-with-nginx-and-php-fpm-on-ubuntu-14-04
- https://www.google.com/search?q=php-fpm+shared+hosting&oq=php-fpm+on+shared+hosting
- [ ] Nginx not reloaded after config changed
- [ ] Disable, rename and delete site
- [ ] DNS
- [ ] PHP select
- [ ] DKIM



# Setup new site
1. Copy sites/_site_template.yml to sites/`site_user`.yml
2. Add role to sites.yml: ```- { role: site, site_vars_file: sites/site_user.yml }```
3. Exec playbook: ```ansible-playbook sites.yml -v```
