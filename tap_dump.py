#!/usr/bin/env python

import os
import sys
import string
import asyncore
import signal
import getopt
import struct
import base64

import mc_bin_server
import mc_bin_client

from memcacheConstants import REQ_MAGIC_BYTE, RES_MAGIC_BYTE
from memcacheConstants import REQ_PKT_FMT, RES_PKT_FMT, MIN_RECV_PACKET
from memcacheConstants import SET_PKT_FMT, DEL_PKT_FMT, INCRDECR_RES_FMT

import memcacheConstants

import tap

def usage(err=0):
    print >> sys.stderr, """
Usage: %s [-u bucket_user [-p bucket_password]] host:port [... hostN:portN]

Example:
  %s -u user_profiles -p secret9876 membase-01:11210 membase-02:11210
""" % (os.path.basename(sys.argv[0]),
       os.path.basename(sys.argv[0]))
    sys.exit(err)

def parse_args(args):
    user = None
    pswd = None

    try:
        opts, args = getopt.getopt(args, 'hu:p:', ['help'])
    except getopt.GetoptError, e:
        usage("ERROR: " + e.msg)

    for (o, a) in opts:
        if o == '--help' or o == '-h':
            usage()
        elif o == '-u':
            user = a
        elif o == '-p':
            pswd = a
        else:
            usage("ERROR: unknown option - " + o)

    if not args or len(args) < 1:
        usage("ERROR: missing at least one host:port to TAP")

    return user, pswd, args

def signal_handler(signal, frame):
    print 'Tap stream terminated by user'
    sys.exit(0)

def mainLoop(serverList, cb, opts={}, user=None, pswd=None):
    """Run the given callback for each tap message from any of the
    upstream servers.

    loops until all connections drop
    """
    signal.signal(signal.SIGINT, signal_handler)

    connections = (tap.TapDescriptor(a) for a in serverList)
    tap.TapClient(connections, cb, opts=opts, user=user, pswd=pswd)
    asyncore.loop()

def parse_mutation_extra(extra):
    engine_priv, flags, ttl, _, _, _, item_flags, item_expiry = struct.unpack(">2h4c2I", extra)
    return {'engine_priv': engine_priv,
            'flags': flags,
            'ttl': ttl,
            'item_flags': item_flags,
            'item_expiry': item_expiry}

if __name__ == '__main__':
    user, pswd, args = parse_args(sys.argv[1:])

    def cb(identifier, cmd, extra, key, vb, val, cas):
        if memcacheConstants.COMMAND_NAMES[cmd] == 'CMD_TAP_MUTATION':
            extra_data = parse_mutation_extra(extra)
            print "%s\t%s\t%s" % (key, base64.b64encode(val), extra_data['item_expiry'])

    opts = {memcacheConstants.TAP_FLAG_DUMP: ''}

    mainLoop(args, cb, opts, user, pswd)
