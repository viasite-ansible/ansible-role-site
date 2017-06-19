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
- setup DKIM keys for domain email (depends of viasite-ansible.exim4)



## Dependencies
- viasite-ansible.apache-vhosts (that depends to viasite-ansible.apache)
- viasite-ansible.cron
- viasite-ansible.exim4 (for DKIM keys)
- viasite-ansible.git
- viasite-ansible.mysql
- viasite-ansible.nginx-vhosts (that depends to viasite-ansible.nginx)
- viasite-ansible.ssh-keys
- viasite-ansible.vim
- viasite-ansible.zsh



## TODO:
- letsencrypt
- add site to hosts_sites
- disable and delete site
- DNS
- apache: PHP select



## Nginx templates:
- `default`
- `default_https`
- `drupal` - based on https://github.com/perusio/drupal-with-nginx
- `joomla`

If you want to enable nginx -> PHP-FPM without apache, set `site_nginx_backend: php-fpm`. It tested lightly only with drupal 7,
/index.php don't work. 

#### Template overrides
All templates support custom code:

- `site_nginx_custom_http` - at `http` context
- `site_nginx_custom_server` - at `server` context
- `site_nginx_custom_root_location` - at `location /` context

Example:
```
server example.com {
  location / {
    # template directives

    {{ site_nginx_custom_root_location }}
  }

  # template directives

  {{ site_nginx_custom_server }}
}

{{ site_nginx_custom_http }}
```



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



## Setup multiple sites
You should not do this:
``` yaml
- hosts: all
  roles:
    - { name: ansible-role-site, site_vars_file: sites/site1.yml }
    - { name: ansible-role-site, site_vars_file: sites/site2.yml }
    - { name: ansible-role-site, site_vars_file: sites/site2_2.yml }
```
If sites/site1.yml defines `site_sync_files_force` and site2.yml have not defined `site_sync_files_force`,
then variable from site1.yml will affect site2! Be careful, run each site separately! Use ansible-site script.



## Change main site domain
1. Change domain in `site_domain`
2. Define old domain at `site_domains_remove`
3. Move site directory to new place (you can also leave site at old path, define `site_root` for that)
4. Exec playbook



## Syncronization

### Import files
Role support import site files from local path or remote sftp server using `rsync`.
You must have access to remote server with ssh key.

#### Variables:
- `site_sync_files` - sync files if directory empty (sync once)
- `site_sync_files_force` - sync files if directory not empty (sync always)
- `site_sync_files_excluded` - exclude patterns (rsync format)
- `site_src` - object that describes files source
- `site_src.path` - remote (or local) path, required
- `site_src.host` - remote host, for remote sync
- `site_src.user` - remote user, for remote sync

Examples:
#### Sync once from remote:
``` yaml
site_sync_files: yes
site_src:
  host: old.site.location
  user: old_user
  path: /old/remote/site/path
```

#### Sync once from remote with some excluded (rsync excluded patterns):
``` yaml
site_sync_files: yes
site_sync_files_excluded:
  - cache/*
  - *.log
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
