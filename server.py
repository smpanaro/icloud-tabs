#!/usr/bin/python

try:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
except:
    from http.server import HTTPServer, BaseHTTPRequestHandler

import update
import json

class TabServer(BaseHTTPRequestHandler):

    def do_POST(self):
        content_len = int(self.headers['content-length'])
        body = self.rfile.read(content_len)

        update.update_tabs(json.loads(body))

        self.send_response(200)
        self.end_headers()
        self.wfile.write("OK".encode('utf-8'))

# start server
port = 8080
server = HTTPServer(('localhost', port), TabServer)
print("Server running on port localhost:{}".format(port))
server.serve_forever()
