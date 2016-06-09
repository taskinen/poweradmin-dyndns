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
r = requests.get( config['default']['ip_lookup_url'] )
if r.status_code is not 200:
  print( "Error finding external IP from output: " + r.text )
  sys.exit(1)
ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', r.text )[0]
print( "Current external IP: " + ip )

# Update IP
url = config['default']['poweradmin_url'] + '/dynamic_update.php' + '?hostname=' + config['default']['domain']+ '&myip=' + ip
r = requests.get( url, auth=( config['default']['login'], config['default']['password'] ) )
print( "Poweradmin says: " + r.text )
