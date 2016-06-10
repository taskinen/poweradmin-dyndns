#!/usr/bin/env python3

import requests
import configparser
import sys
import re

# Read and parse configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Check that Poweradmin URL uses HTTPS since what we are doing is not secure otherwise
if config['default']['poweradmin_url'][:8] != "https://":
  print( "ERROR: Refusing to use insecure non-https Poweradmin URL: " + config['default']['poweradmin_url'] )
  sys.exit(1)

# Find external IP
if config['default'].getboolean('verbose'):
  print( "Querying public IP from: " + config['default']['ip_lookup_url'] )
r = requests.get( config['default']['ip_lookup_url'] )
if r.status_code is not 200:
  print( "ERROR: Querying external IP failed with response " + r.status_code )
  sys.exit(1)
ip = re.search( r'[0-9]+(?:\.[0-9]+){3}', r.text )
if ip:
  if config['default'].getboolean('verbose'):
    print( "Current external IP: " + ip.group(0) )
else:
  print( "ERROR: Not able to parse external IP from output: " + ip.string )
  sys.exit(1)

# Update IP
url = config['default']['poweradmin_url'] + '/dynamic_update.php' + '?hostname=' + config['default']['domain']+ '&myip=' + ip.group(0)
if config['default'].getboolean('verbose'):
  print( "Updating hostname " + config['default']['domain'] + " point to " + ip.group(0) + " using " + url )
r = requests.get( url, auth=( config['default']['login'], config['default']['password'] ) )
if r.text.strip() != "good":
  print( "ERROR: Not able to update hostname. Poweradmin responded: " + r.text.strip() )
  sys.exit(1)
elif config['default'].getboolean('verbose'):
  print( "Poweradmin responds: " + r.text.strip() )

sys.exit(0)
