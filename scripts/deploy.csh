#!/bin/csh
#------------------------------------------------------------------------------#
# deploy.csh                                                                   #
#------------------------------------------------------------------------------#
# By: Bartlomiej Mika
# Date: April, 27th, 2015
#
# Description:
# This script will load up the django virtual environment instance
# and start the web-server.
#
# Prerequsites:
# (1) Running on FreeBSD OS
# (2) Running in user called 'freebsd'
# (3) AcademicsToday dir: /usr/home/freebsd/py-academicstoday
#
#----------------#
# HOWTO: Setup:  #
#----------------#
# (1) Give permission
# $ chmod u+x /usr/home/freebsd/py-academicstoday/scripts/deploy.csh
#
# (1) Run command:
# $ /usr/home/freebsd/py-academicstoday/scripts/deploy.csh

# Clear all text on the screen
clear;

# Turn on virtual environment
source /usr/home/freebsd/py-academicstoday/env/bin/activate.csh

# Bugfix
ln -s /usr/home/freebsd/py-academicstoday/env/lib/python3.4/site-packages/django/contrib/admin/static/admin /usr/home/freebsd/py-academicstoday/academicstoday_project/static/admin

# Run command
cd /usr/home/freebsd/py-academicstoday/academicstoday_project
gunicorn -c gunicorn_config.py academicstoday_project.wsgi
