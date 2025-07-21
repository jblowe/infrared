import sys
import os

sys.path.insert(0, '/home/ubuntu/tap-infrared')
os.chdir('/home/ubuntu/tap-infrared')

from bottle import default_app
import app  # registers your routes

application = default_app()
