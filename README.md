[![Build Status](https://travis-ci.org/viasite-ansible/ansible-role-site.svg?branch=master)](https://travis-ci.org/viasite-ansible/ansible-role-site)

# ansible-role-site
Ansible role for setup php site.

Role has many dependencies to other viasite-ansible roles, so I don't think that you can easy use it.

- sites/*.yml - each yml = site



## Features
- setup user for site
- nginx -> apache -> PHP-FPM (with .htaccess support)
- nginx -> PHP-FPM (without .htaccess support, experimental)
- import site from remote host
- setup mysql with import from remote sql dump
- setup cron tasks
- optimized for Drupal sites



## Dependencies
- viasite-ansible.apache-vhosts (that depends to viasite-ansible.apache)
- viasite-ansible.cron
- viasite-ansible.git
- viasite-ansible.mysql
- viasite-ansible.nginx-vhosts (that depends to viasite-ansible.nginx)
- viasite-ansible.ssh-keys
- viasite-ansible.vim
- viasite-ansible.zsh



## TODO:
- SSL, letsencrypt
- add site to hosts_sites
- disable, rename and delete site
- DNS
- apache: PHP select
- DKIM
- tests



## Nginx templates:
- `default`
- `drupal` - based on https://github.com/perusio/drupal-with-nginx
- `joomla`

If you want to enable nginx -> PHP-FPM without apache, set `site_nginx_backend: php-fpm`. It tested lightly only with drupal 7,
/index.php don't work. 

## PHP-FPM settings
Use `site_php_fpm_extras` variable:
``` yaml
site_php_fpm_extras:
  "php_admin_value[memory_limit]": 512M
```



## Setup new site
1. Copy sites/_site_template.yml to sites/`site_user`.yml
2. Add role to sites.yml: ```- { role: site, site_vars_file: sites/site_user.yml }```
3. Exec playbook: ```ansible-playbook sites.yml -v```



## Syncronization

### Import files
Role support import site files from local path or remote sftp server using `rsync`.

Examples:
#### Sync once from remote:
``` yaml
site_sync_files: yes
site_src:
  host: old.site.location
  user: old_user
  path: /old/remote/site/path
```

#### Sync once from local:
``` yaml
site_sync_files: yes
site_src:
  path: /old/local/site/path
```

#### Sync always from local:
``` yaml
site_sync_files: yes
site_sync_files_force: yes
site_src:
  path: /old/local/site/path
```


### Import MySQL database
You can import database from sql dump local path or remote sftp server using `rsync`.
Supported formats: `.sql`, `.bz`, `.gz`, `.xz`.

Examples:
#### Sync once from remote:
``` yaml
site_sync_mysql: yes
site_src_mysql_dump_file:
  host: old.site.location
  user: old_backup_user
  path: /path/to/remote/dump
```

#### Sync always from remote:
``` yaml
site_sync_mysql: yes
site_sync_mysql_force: yes
site_src_mysql_dump_file:
  host: old.site.location
  user: old_backup_user
  path: /path/to/remote/dump
```


## Example playbook
