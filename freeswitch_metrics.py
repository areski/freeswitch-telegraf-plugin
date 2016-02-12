#!/usr/bin/env python
"""
FreeSWITCH Metrics

This script collects the following FreeSWITCH metrics:
    - total of active channels
    - total of calls
    - Current CPS

Usage:

    export FS_HOST=localhost; export FS_PORT=8080; export FS_USERNAME=freeswitch; export FS_PASSWORD=works
    ./freeswitch_metrics.py

"""

from xmlrpclib import ServerProxy
from datetime import datetime
import re
import os

# Connectiong settings for FreeSWITCH XML RPC
FS_HOST = os.getenv('FS_HOST', 'localhost')
FS_PORT = os.getenv('FS_PORT', 8080)
FS_USERNAME = os.getenv('FS_USERNAME', 'freeswitch')
FS_PASSWORD = os.getenv('FS_PASSWORD', 'works')

DEMO_MODE = False

server = ServerProxy("http://%s:%s@%s:%s" % (FS_USERNAME,
                                             FS_PASSWORD,
                                             FS_HOST,
                                             FS_PORT))


def get_calls():
    """
    Connect to FreeSWITCH server and get calls count

    fs_cli -x "show channels count"

    0 total.
    """
    calls = server.freeswitch.api("show", "calls count")
    num_calls = r'\n(?P<chans>\d+) total\.\n'
    regexp = re.compile(num_calls)
    matches = regexp.search(calls)
    return int(matches.group("chans"))


def get_channels_cps():
    """
    Connect to FreeSWITCH server and get channels count & cps

    fs_cli -x "show status"
    UP 0 years, 9 days, 2 hours, 56 minutes, 28 seconds, 402 milliseconds, 835 microseconds
    FreeSWITCH (Version 1.6.6 -13-d2d0b32 64bit) is ready
    5893 session(s) since startup
    0 session(s) - peak 7, last 5min 1
    0 session(s) per Sec out of max 60, peak 6, last 5min 1
    1200 session(s) max
    min idle cpu 0.00/97.17
    Current Stack Size/Max 240K/8192K
    """
    status = server.freeswitch.api("show", "status")
    # lines = status.splitlines()
    # lines[5]
    num_channels = r'(?P<sessions>\d+) \w.* - peak'
    regexp = re.compile(num_channels)
    matches = regexp.search(status)
    sessions = int(matches.group("sessions"))
    num_cps = r'(?P<cps>\d+) \w.* per Sec'
    regexp = re.compile(num_cps)
    matches = regexp.search(status)
    cps = int(matches.group("cps"))
    return (sessions, cps)


def print_statics():
    try:
        n_calls = get_calls()
        (sessions, cps) = get_channels_cps()
    except:
        n_calls = 0
        sessions = 0
        cps = 0
    print("{\"active_channels\": %d, \"active_calls\": %d, \"cps\": %d}" % (sessions, n_calls, cps))


if __name__ == "__main__":
    if DEMO_MODE:
        dt = datetime.now()
        n_calls = dt.minute
        sessions = dt.minute
        cps = dt.second
        print("{\"active_channels\": %d, \"active_calls\": %d, \"cps\": %d}" % (sessions, n_calls, cps))
    else:
        print_statics()
