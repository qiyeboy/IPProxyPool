# coding:utf-8
import BaseHTTPServer
import json
import urlparse


class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        """
        """
        print
        self.path
        parsed_path = urlparse.urlparse(self.path)
        print
        parsed_path
        print
        parsed_path.query
        # message_parts = [
        # 'CLIENT VALUES:',
        # 'client_address=%s (%s)' % (self.client_address,
        # self.address_string()),
        #         'command=%s' % self.command,
        #         'path=%s' % self.path,
        #         'real path=%s' % parsed_path.path,
        #         'query=%s' % parsed_path.query,
        #         'request_version=%s' % self.request_version,
        #         '',
        #         'SERVER VALUES:',
        #         'server_version=%s' % self.server_version,
        #         'sys_version=%s' % self.sys_version,
        #         'protocol_version=%s' % self.protocol_version,
        #         '',
        #         'HEADERS RECEIVED:',
        #         ]
        # for name, value in sorted(self.headers.items()):
        #     message_parts.append('%s=%s' % (name, value.rstrip()))
        # message_parts.append('')
        # message = '\r\n'.join(message_parts)
        data1 = [{'ip': '192.168.0.0', 'port': 456}] * 10
        d1 = json.dumps(data1, sort_keys=True, indent=4)
        message = ('192.168.1.1', 80)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(d1)


server = BaseHTTPServer.HTTPServer(('0.0.0.0', 8000), WebRequestHandler)
server.serve_forever()