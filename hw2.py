#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import cgi
import numpy as np
from pandas import DataFrame

d = {"metric":[], "value":[], "time":[]}

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def genJSON(self,df,name):
        c = df[df["metric"] == name]
        a = c["value"]
        na = np.array(a)
        b = c["time"].values.tolist()
        return '{"count":' + str(len(a)) + ',"timeRange": {"start":' + str(b[0]) + ',"end":' + str(b[len(b)-1]) + '},"maxValue":' + str(max(a)) + ',"minValue":' +  str(min(a)) + ',"averageValue":' + str(np.mean(na)) + ',"standardDeviation":' + str(np.std(na)) + ',"25thPercentile":' + str(np.percentile(na,25))  + ',"50thPercentile":' + str(np.percentile(na,50))  + ',"75thPercentile":' + str(np.percentile(na,75)) + ',"99thPercentile":' + str(np.percentile(na,99)) + '}'

    def do_GET(self):
        self._set_headers()
        print self.path
        if (self.path == '/hello') :
            self.wfile.write('{"message":"Hello World!"}')
        elif (self.path.startswith('/stats')) :
            global d
            df = DataFrame(d)
            name = self.path.split('/')[2]
            self.wfile.write(self.genJSON(df,name))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        rf = self.rfile
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':'text/plain',
                     })
        st = form.value.split('\n')
        global d
        d["metric"] = []
        d["value"] = []
        d["time"] = []
        for item in st:
            if len(item) == 0 :
                continue
            vs = item.split(' ')
            d["metric"].append(vs[0])
            d["value"].append(float(vs[1]))
            d["time"].append(int(vs[2]))

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
