# poweradmin-dyndns
This script updates a given PowerDNS controller hostname dynamically with the current publicly visible external IP address.

## Pre-requisites

Tested Poweradmin version is 2.1.7, but any newer should work.

Python 3, tested with Python 3.5.1 on Ubuntu 16.04.

Python 3 packages `requests` and `configparser`. If you don't have them, install them with `pip`. Packages `re` (regular expressions handling package) and `sys` should be universally available with Python 3.

## Configuration

To use this script, configure config.ini file as shown in config.ini.example:

```ini
[default]
login = MyUsername
password = MyPassword
domain = myhostname.domain.tld
poweradmin_url = https://example.com/poweradmin
ip_lookup_url = http://checkip.dy.fi/
verbose = True
```

`login` is your Poweradmin username, `password` is your password, `domain` is your hostname with full domainname which you want point to your current IP address.

You must know the URL of your hosting provider's Poweradmin control panel (usually ends with /poweradmin), set that as `poweradmin_url`.

You can use any publicly available IP-checking tool, which outputs your external IP address as plain text. This script will try to parse its output and use the first IPv4 looking IP address. In the configuration example `ip_lookup_url` is defined as `http://checkip.dy.fi/` which I have found satisfactory. Feel free to use your own.

If you want verbose output, set `verbose` to `True`, otherwise `False`.
