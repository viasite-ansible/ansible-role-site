# ansible-role-site
Ansible role for setup php site.

- sites/*.yml - each yml = site


# Setup new site
1. Copy sites/_site_template.yml to sites/`site_user`.yml
2. Add role to sites.yml: ```- { role: site, vars_file: sites/site_user.yml }```
3. Exec playbook: ```ansible-playbook sites.yml -v```

# TODO
- [ ] Nginx not reloaded after config changed
- [ ] Disable, rename and delete site
- [ ] DNS
- [ ] PHP select
