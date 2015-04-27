#!/bin/csh
#------------------------------------------------------------------------------#
# checkinbox.csh                                                               #
#------------------------------------------------------------------------------#
# By: Bartlomiej Mika
# Date: April, 23th, 2015
#
# Description:
# This script will load up the django virtual environment instance
# and run the 'checkinbox' command.
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
# $ chmod u+x /usr/home/freebsd/py-academicstoday/scripts/checkinbox.csh
#
# (1) Run command:
# $ crontab -e
#
# (2) This makes cron job run once every day:
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 0 0 * * * ./usr/home/freebsd/py-academicstoday/scripts/checkinbox.csh
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Clear all text on the screen
clear;

# Turn on virtual environment
source /usr/home/freebsd/py-academicstoday/env/bin/activate.csh

# Run command
python /usr/home/freebsd/py-academicstoday/academicstoday_project/manage.py checkinbox

# Turn off virtual environment
deactivate