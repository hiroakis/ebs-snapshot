#!/usr/bin/python

import boto.ec2
import requests
import re
import argparse
import logging
import sys

META_DATA_ENDPOINT = "http://169.254.169.254/latest/meta-data/"

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n', '--number',
        dest = 'number',
        nargs = '?',
        default = 3,
        required = False,
        type = int,
        help = 'The number of snapshot generations. \
            Older snapshots will be deleted than number of generations. default: 3'
    )
    parser.add_argument(
        '-l', '--log',
        dest = 'log',
        nargs = '?',
        default = '/tmp/ebs_snapshot.log',
        required = False,
        type = str,
        help = 'Log file. default: /tmp/ebs_snapshot.log'
    )
    return parser.parse_args()

def get_connection():
    url = META_DATA_ENDPOINT + "placement/availability-zone"
    az = requests.get(url).text
    region = re.sub(r'.$', '', az)
    return boto.ec2.connect_to_region(region)

def get_instance_id():
    url = META_DATA_ENDPOINT + "instance-id"
    return requests.get(url).text

def create_snapshots(volumes):
    for volume in volumes:
        desc = "volume(%s) on instance %s" % (str(volume.id), str(get_instance_id()))
        msg = "create snapshot from volume(%s)" % str(volume.id)
        logging.info(msg)
        volume.create_snapshot(description=desc)

def delete_old_snapshots(volumes, number):
    for volume in volumes:
        snapshots = sorted(volume.snapshots(), key=lambda x:x.start_time, reverse=True)
        for i, snapshot in enumerate(snapshots):
            if number <= i:
                msg = "delete snapshot: %s %s" % (str(snapshot.id), snapshot.start_time)
                logging.info(msg)
                snapshot.delete()

opts = get_options()

# The logging module is not only used in this code but also used by boto
logging.basicConfig(filename=opts.log,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y/%m/%d %I:%M:%S',
    level=logging.INFO
    )

logging.info("start")

exit_code = 0
try:
    con = get_connection()
    volumes = con.get_all_volumes(filters={'attachment.instance-id': get_instance_id()})

    create_snapshots(volumes)
    delete_old_snapshots(volumes, opts.number)
except Exception as e:
    exit_code = 1
    logging.exception(e.message)

logging.info("end")
sys.exit(exit_code)
