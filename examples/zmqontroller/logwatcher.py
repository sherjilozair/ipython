#!/usr/bin/env python
"""A simple log process that prints messages incoming from"""

#
#    Copyright (c) 2010 Min Ragan-Kelley
#
#    This file is part of pyzmq.
#
#    pyzmq is free software; you can redistribute it and/or modify it under
#    the terms of the Lesser GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    pyzmq is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    Lesser GNU General Public License for more details.
#
#    You should have received a copy of the Lesser GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import zmq
logport = 20201
def main(topics, addrs):
    
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    for topic in topics:
        socket.setsockopt(zmq.SUBSCRIBE, topic)
    if addrs:
        for addr in addrs:
            print "Connecting to: ", addr
            socket.connect(addr)
    else:
        socket.bind('tcp://127.0.0.1:%i'%logport)

    while True:
        # topic = socket.recv()
        # print topic
        topic, msg = socket.recv_multipart()
        # msg = socket.recv_pyobj()
        print "%s | %s " % (topic, msg),

if __name__ == '__main__':
    import sys
    topics = []
    addrs = []
    for arg in sys.argv[1:]:
        if '://' in arg:
            addrs.append(arg)
        else:
            topics.append(arg)
    if not topics:
        # default to everything
        topics = ['']
    if len(addrs) < 1:
        print "binding instead of connecting"
        # addrs = ['tcp://127.0.0.1:%i'%p for p in range(logport,logport+10)]
    #     print "usage: display.py <address> [ <topic> <address>...]"
        # raise SystemExit
    
    main(topics, addrs)