#!/usr/bin/env python
# coding=utf-8

import argparse
import socket
import sys
from BaseHTTPServer import BaseHTTPRequestHandler

from urllib import quote


class RouteHandler(BaseHTTPRequestHandler):
    method = None
    url = None
    response = None

    def handle_api(self):
        if self.command != self.method:
            self.send_error(501, "Unsupported method (%r)" % self.command)
            return
        if self.path != self.url:
            self.send_error(404, "File not found.")
            return
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(self.response.encode("utf-8"))

    def handle_one_request(self):
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = 1
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            self.handle_api()
            self.wfile.flush()  # actually send the response if not already done.
        except socket.timeout, e:
            # a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return


def run(host, port, url, method, response):
    # Start a simple server, and loop forever
    from BaseHTTPServer import HTTPServer
    RouteHandler.url = quote(url.encode("utf-8"))
    RouteHandler.response = unicode(response)
    RouteHandler.method = method.upper()

    server = HTTPServer((host, port), RouteHandler)
    print "The following api is running, use <Ctrl-C> to stop"
    print method.upper() + " http://" + host + ":" + str(port) + quote(url.encode("utf-8"))
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Auto verification based rest")
    parser.add_argument('url', type=lambda s: s.decode(sys.getfilesystemencoding()), help=u"url地址，例如 /user/login ")
    parser.add_argument('response', type=lambda s: s.decode(sys.getfilesystemencoding()),
                        help=u'返回值，如果有返回值有空格，请用引号将返回值内容括起来')
    parser.add_argument("--host", default="localhost", help=u'监听地址')
    parser.add_argument('-p', "--port", type=int, default=3000, help=u'监听端口')
    parser.add_argument('-m', '--method', default="GET", help=u"指定HTTP方法，默认为GET")
    args = parser.parse_args()
    try:
        run(args.host, args.port, args.url, args.method, args.response)
    except KeyboardInterrupt as e:
        print u"结束运行"


if __name__ == '__main__':
    main()
