import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def assert_cmd_text(Command, cmd, assert_text, error_text=''):
    html = Command.check_output(cmd)
    assert assert_text in html, error_text


def test_sync_files(File):
    c = File('/home/site1/www/site1.example.com/excluded_dir/file.php')
    assert not c.exists
    c = File('/home/site1/www/site1.example.com/excluded_file.php')
    assert not c.exists


def test_apache_nginx_php(Command):
    c = Command

    # index file
    assert_cmd_text(c, "curl site1.example.com/index.php", "index content")
    assert_cmd_text(c, "curl site1.example.com/", "index content")

    # redirect
    assert_cmd_text(c, "curl -I site1.example.com/redirect-test/", "301 Moved")
    assert_cmd_text(c, "curl -L site1.example.com/redirect-test/",
                    "index content")

    # image.png
    html = Command.check_output("curl -I site1.example.com/image.png")
    assert "Server: nginx" in html
    assert "200 OK" in html

    # phpinfo.php
    assert_cmd_text(c, "curl -I site1.example.com/phpinfo.php", "200 OK")

    # restricted .htaccess
    assert_cmd_text(c, "curl -I site1.example.com/.htaccess", "404 Not Found")

    # restricted git
    c("git init /home/site1/www/site1.example.com")
    assert_cmd_text(c, "curl -I site1.example.com/.git/config",
                    "403 Forbidden")


def test_users(Command):
    c = Command

    # access to own file
    cmd = c("su site1 -c 'cat /home/site1/www/site1.example.com/index.php'")
    assert cmd.rc == 0

    # access to foreign file
    cmd = c("su site2 -c 'cat /home/site1/www/site1.example.com/index.php'")
    assert cmd.rc == 1

    # create file in home
    cmd = c("su site1 -c 'touch /home/site1/testfile'")
    assert cmd.rc == 0
    c("su site1 -c 'rm /home/site1/testfile'")


def test_cron(Command):
    c = Command('crontab -l -u site1').stdout
    assert 'MAIL=mail@site1.example.com' in c
    assert '#Ansible: site1: scripts' in c
    assert '10 * * * * env >/dev/null 2>&1' in c
