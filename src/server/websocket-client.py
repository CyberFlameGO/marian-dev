#!/usr/bin/env python

from __future__ import print_function, unicode_literals, division

import sys,time,argparse,regex

from websocket import create_connection


if __name__ == "__main__":
    # handle command-line options
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--batch-size", type=int, default=1)
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("file",type=file,nargs='?')
    args = parser.parse_args()
    print("PORT: %d"%args.port)

    # open connection
    ws = create_connection("ws://localhost:{}/translate".format(args.port))

    count = 0
    batch = ""
    linectr = 0

    if args.file:
        text = regex.sub(r'\n',r'\\n',args.file.read())
        count = 1
        payload = '{ "id": %d, "text": "%s"}'%(count, text.decode('utf8'))
        print(payload)
        ws.send('{ "id": %d, "text": "%s"}'%(count, text.decode('utf8')))
    else:        
        for line in sys.stdin:
            count += 1
            ws.send('{ "id": %d, "text": "%s"}'%(count, line.decode('utf8').strip()))

    while count:
        result = ws.recv()
        print(result)
        count -= 1
    # close connection
    ws.close()
