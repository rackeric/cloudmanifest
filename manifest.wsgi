import sys, os
sys.path.insert (0,'/var/www/html/cloudmanifest')
os.chdir("/var/www/html/cloudmanifest")
from manifest import create_app as application
