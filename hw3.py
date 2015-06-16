#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import cgi
import numpy as np

a = []
b = []

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        print self.path
        if (self.path == '/hello') :
            self.wfile.write('{"message":"Hello World!"}')
        elif (self.path.startswith('/stats')) :
            ps = self.path.split('=&')
            for s in ps:
                print s
            global a
            na = np.array(a)
            self.wfile.write('{"count":' + str(len(a)) + ',"timeRange": {"start":' + str(b[0]) + ',"end":' + str(b[len(b)-1]) + '},"maxValue":' + str(max(a)) + ',"minValue":' +  str(min(a)) + ',"averageValue":' + str(np.mean(na)) + ',"99thPercentile":' + str(np.percentile(na,99)) + '}')

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        rf = self.rfile
        print type(rf)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':'text/plain',
                     })
        st = form.value.split('\n')
        global a
        global b
        a = []
        b = []
        for item in st:
            if len(item) == 0 :
                continue
            vs = item.split(' ')
            a.append(float(vs[0]))
            b.append(int(vs[1]))
        print a
        print b

def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
