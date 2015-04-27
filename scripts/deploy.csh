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

# Run command
gunicorn -c gunicorn_config.py /usr/home/freebsd/py-academicstoday/academicstoday_project/academicstoday_project.wsgi
