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
- install drupal with your settings (depends of viasite-ansible.drupal)
- setup mysql with import from remote sql dump
- setup posrgresql with import from remote sql dump
- setup cron tasks
- optimized for Drupal sites
- setup DKIM keys for domain email (depends of viasite-ansible.exim4)
- add domain to Selectel DNS with viasite/selectel-dns-cli
- install solr in docker on custom domain



## Dependencies
- viasite-ansible.apache-vhosts (that depends to viasite-ansible.apache)
- viasite-ansible.cron
- viasite-ansible.exim4 (for DKIM keys)
- viasite-ansible.git
- viasite-ansible.mysql
- viasite-ansible.nginx-vhosts (that depends to viasite-ansible.nginx)
- viasite-ansible.postgresql
- viasite-ansible.ssh-keys
- viasite-ansible.vim
- viasite-ansible.zsh
- viasite-ansible/ansible-molule-selectel-dns for Selectel DNS
- docker on target machine (for Solr)



## TODO:
- add site to hosts_sites
- disable and delete site



## Nginx engines (`site_nginx_engine`):
- `default`
- `drupal` - based on https://github.com/perusio/drupal-with-nginx
- `joomla`
- `service` - required `site_nginx_service_port

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



## PHP version select
You can use viasite-ansible.php-versions role for install several PHP versions from `ondrej/php`,
then you can define `site_php_version` in site config.



## PHP-FPM settings
Use `site_php_fpm_extras` variable:
``` yaml
site_php_fpm_extras:
  "php_flag[display_startup_errors]": "on"
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

### Sync mysql
By default, `site_sync_mysqldump: yes` and ansible dump remote database before sync.

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


### Manage Selectel DNS
You must install viasite-ansible/ansible-module-selectel-dns for use this feature.

Check default variables `site_dns_*` in `defaults/main.yml`.
Common variable: `site_dns_domain` - domain for adding. Default: `site_domain`
In common case, you can only define `site_selectel_dns`.

By default, DNS tasks don't executing, you should using `--tags dns`.

Example:

``` yaml
site_dns_domains:
  example.com:
    - record: ''
      type: A
      value: 1.2.3.4
    - record: '*'
      type: A
      value: 1.2.3.4
      ttl: 300
    - record: 'www'
      type: A
      value: 1.2.3.4
    - record: 'old'
      type: A
      value: 1.2.3.4
      state: absent
```


### Issue letsencrypt certificate
Define variables:

- `site_letsencrypt_acmesh_args` - args for acme.sh --issue command (optional)
- `site_letsencrypt_acmesh_deploy_path` - deploy path (optional)
- `site_letsencrypt_acmesh_domains` - list of domains


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


## Install Solr
Requires Docker on target machine.
``` yaml
site_solr: yes

# Core name must be unique in server scope
# Recommended name: {{ site_user }}
site_solr_core_name: drupal

# External port for local nginx-solr connection
# Must be unique in server scope
# For site Solr port always be 80
site_solr_port: 8983

# Solr domain
# You should add 'IN A' record to DNS youself
site_solr_domain:

# Basic auth string generated by `htpasswd -nb user password` (пакет apache2-utils)
# Leave plain password in comment
site_solr_basic_auth: '' # generate with htpasswd -nb user password # jKWeyVgono2x

# URL or local path to solr config (contents of directory search_api_solr/solr-conf/5.x/)
site_solr_config_archive:
```
