import sys, os

activate_this = '/var/www/html/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert (0,'/var/www/html/cloudmanifest')

from manifest import create_app as application
