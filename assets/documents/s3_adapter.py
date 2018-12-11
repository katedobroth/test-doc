#!/usr/bin/env python
# Copyright (c) 2016 Cazena, Inc., as an unpublished work.
## This notice does not imply unrestricted or public access to these
## materials which are a trade secret of Cazena, Inc. or its
## subsidiaries or affiliates (together referred to as "Cazena"), and
## which may not be copied, reproduced, used, sold or transferred to any
## third party without Cazena's prior written consent.
##
## All rights reserved.

# Python script for S3 custom adapter

# This script uses Boto, an Amazon Web Services API for python.

# SEE:  https://spin.atomicobject.com/2014/09/24/automate-amazon-s3-python/ 
#   and https://github.com/boto/boto3
#   and https://boto.readthedocs.io/en/latest/

# Install Boto with the command:
# NOTE:   prerequisite is the python package manager pip
#         SEE: https://pip.pypa.io/en/stable/installing/ for 
#         instructions on installing pip, if not already on a system
#   > pip install boto

import sys
import os
import time
import boto
import boto.s3.connection
# from boto.s3.connection import S3Connection
from boto.s3.connection import Key
import ConfigParser
import argparse
import logging
# from time import sleep
import signal

# EXAMPLE:  s3_adapter.py [ -pgm_args "<adapter specific args>" ] 
#                         [ -list | 
#                           -move <entname> [ -rows <rowsnum> ] | 
#                           -version ] 

# EXAMPLES:  
#   s3_adapter.py -pgm_args "~/s3_adapter.ini" -move bankemps.dsv
#   s3_adapter.py -pgm_args "~/s3_adapter.ini" -list
#   s3_adapter.py -pgm_args "~/s3_adapter.ini" -version

# The optional adapter specific arg is:
#   -- the name of the configuration (.ini) file
#   -- defaults to "s3_adapter.ini" in current working directory


# TODO:  May need to add support for region, right now this is not
#        supported in this code.

# declare some global variables so we can clean up the local file in case
# program is terminated by SIGTERM signal
localfile = ""
tempfile = None
cwd = os.path.dirname(os.path.realpath(sys.argv[0]))

def sigterm_handler(signal, frame):
    global tempfile
    log.warn("Program terminated by termination signal prior to completion")    
    # cleanup any local temp file before terminating
    if tempfile:
        tempfile_cleanup()
    log.info("==========  Done Processing Data Adapter for S3, rc = " + str(rc) + " ==========")   
    sys.exit(1)


def tempfile_cleanup():
    global tempfile
    global localfile
    if tempfile != '':
        log.debug("Closing local file: " + localfile)    
        tempfile.close()
        log.debug("Deleting local file: " + localfile)
        os.remove(localfile)


def logger_setup():
    # Set up python logger
    log = logging.getLogger('s3_adapter')
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logfileName = cwd + "/s3_adapter.log"
    fh = logging.FileHandler(logfileName)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)
    return log


def s3_connect(access_key, secret_key):
    log.debug("Connecting to S3 using call to boto.connect_s3")
    try:
        conn = boto.connect_s3(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key)
        if conn:
            return conn
    except Exception, e:
        msg = "Unable to connect to AWS S3 bucket, verify credentials in the .ini file" 
        print (msg)
        log.error(msg)
        log.error("Exception raised " + format(e))
        return 1


def list_entities(access_key, secret_key, bucketname):
    conn = s3_connect(access_key, secret_key)
    if not conn:
        return 1
    try:    
        bucket = conn.get_bucket(bucketname, validate=False)
        log.debug("Listing files in bucket: %s " % (bucketname) )
        for file_key in bucket.list():
            epochtime = convert_S3time_to_epoch(str(file_key.last_modified) )
            msg = ("%s, %s, %s" % (file_key.name, str(file_key.size), str(epochtime) ) )
            log.debug(msg)
            print (msg)
        return 0
    except Exception, e:
        msg = "Unable to list AWS S3 bucket entities, exception raised" 
        print (msg)
        log.error(msg)
        log.error("Exception raised " + format(e))
        return 1   


def convert_S3time_to_epoch(timestr):
    # time string returned by S3 library looks like:  2016-09-09T14:15:18.000Z
    pattern = '%Y-%m-%dT%H:%M:%S.000Z'
    epochtime = int(time.mktime(time.strptime(timestr, pattern)))
    return epochtime


def show_version():
    print ('1.0')
    return 0


def move_data(access_key, secret_key, bucketname, datafile, numrows): 
    #  If we want to read the file as a URL the URL format would look something
    #  like this:
    #      https://console.aws.amazon.com/s3/home?region=us-east-1#&bucket=lorraine-adapter-test&prefix=
    #  Can then do something like code shown below:
    #      SEE:  https://forums.aws.amazon.com/thread.jspa?threadID=93472

    # import urllib2
    # f = urllib2.urlopen('https://s3.amazonaws.com/mybucket/DL_test/test_input')
    # for line in f.readlines():
    # line = line.rstrip()
    # #print str(line)
    # parts = line.split()
    # print parts[0]

    # But currently this function is NOT reading the S3 file directly.  Instead it
    # is downloading the file to a local file, then processing the local file

    global tempfile
    global localfile

    # Do the actual move of the entity (in this case a file in S3 bucket)
    conn = s3_connect(access_key, secret_key)
    if not conn:
        return 1

    try: 
        bucket = conn.get_bucket(bucketname, validate=False)
    except Exception, e:
        msg = "Unable to access AWS S3 bucket, verify credentials in the .ini file" 
        print (msg)
        log.error(msg)
        log.error("Exception raised " + format(e))
        return 1

    # Download named file to local file
    ts = int(time.time())
    localfile = "tmp_" + str(ts) + "_" + datafile
    log.info("Downloading s3 file: " + datafile + ", to localfile: " + localfile)
    k = Key(bucket)
    k.key = datafile
    k.get_contents_to_filename(localfile)

    # Open file, write to stdout, then close it.  If rows is > 0 then
    # need to limit the number of rows processed to that number
    if numrows:
        log.info("Writing contents of file: " + localfile + " to stdout; limiting to " + str(numrows) + " rows")
    else:    
        log.info("Writing contents of file: " + localfile + " to stdout")

    linecount = 0
    tempfile = file(localfile, "r")
    for line in tempfile.readlines():
        linecount = linecount + 1
        if numrows > 0 and linecount > numrows:
            # processed all the rows requests, so done 
            break
        else:
            # # FOR TESTING
            # # Sleep a while to test enable testing SIGTERM signal
            # print("Sleeping for 5 seconds before processing line: " + str(linecount))
            # sleep(5)           
            print line.rstrip()

    tempfile_cleanup()
    return 0


#####   Main Processing  #####

# declare SIGTERM handler
signal.signal(signal.SIGTERM, sigterm_handler)

# set up python logger
log = logger_setup()
log.info("==========  Starting Custom Data Adapter for S3 ==========")

# Parse arguments 
parser = argparse.ArgumentParser(description='S3 custom adapter to move data from S3 to Cazena Cloud')
parser.add_argument('-pgm_args', nargs='?', metavar='<"adapter_args">', type=str, help='Adapter specific arguments supplied as a single argument in double quotes')
parser.add_argument('-list', action='store_true', help='List entities that this adapter is capable of moving (e.g. files in S3 bucket)')
parser.add_argument('-move', metavar='<entity>', help='Name the entity to be moved')
parser.add_argument('-rows', default=0, type=int, metavar='<rowcount>', help='For MOVE, optionally specify max rows to move')
parser.add_argument('-version', action='store_true', help='Identify the version of the data mover API which is compatible with this adapter')
args = parser.parse_args()

log.debug("Adapter specific args: " + str(args.pgm_args) )
log.debug("List argument supplied: " + str(args.list) )
log.debug("Move entity name: " + str(args.move) )
log.debug("Row count arg: " + str(args.rows) )
log.debug("Version argument supplied: " + str(args.version) )

# Validate argument combinations
if args.list and (args.version or str(args.move) != 'None'):
    msg = "No other action argument allowed with the LIST option"
    print (msg)
    log.error(msg)
    sys.exit(1)

if args.version and (args.list or str(args.move) != 'None'):
    msg = "No other action argument allowed with the VERSION option"
    print (msg)
    log.error(msg)
    sys.exit(1) 

if not args.list and not args.version and str(args.move) == 'None':
    msg = "No action specified, must be LIST, VERSION, or MOVE"
    print (msg)
    log.error(msg)
    sys.exit(1) 


# Deal with adapter specific argument.  In this case there is only one optional argument
# which is the name of the .ini file to read for S3 credentials and other information
if str(args.pgm_args) == 'None' or str(args.pgm_args) == "":
    config_file = cwd + "/s3_adapter.ini" 
else:    
    config_file = args.pgm_args 
    # config_file = ''.join(args.pgm_args)

# Normalize path in case user used ~  or ".." references in the pathname
config_file = os.path.normpath(os.path.expanduser(config_file))

# Make sure .ini file exists
if not os.path.isfile(config_file):
    msg = "Configuration file: " + config_file + " does not exist"
    print (msg)
    log.error(msg)
    sys.exit(1)

# Get data from adapter configuration file (.ini file)
log.info("Reading config file: " + config_file)
Config = ConfigParser.ConfigParser()
Config.read(config_file)
access_key = Config.get('Credentials', 'aws_access_key_id')
secret_key = Config.get('Credentials', 'aws_secret_access_key')
bucketname = Config.get('Data', 'bucketname')
log.info("S3 Bucket: " + bucketname)

# Take action based on program arguments
if args.list:
    rc = list_entities(access_key, secret_key, bucketname)
elif args.version:
    rc = show_version()
elif str(args.move) != 'None':
    datafile = args.move
    rc = move_data(access_key, secret_key, bucketname, datafile, int(args.rows) )

log.info("==========  Done Processing Data Adapter for S3, rc = " + str(rc) + " ==========")
sys.exit(rc)
