"""
Very simple HTTP server in python
Usage::
    ./server.py [<port>]
"""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging


DEFAULT_BUCKET = os.environ.get("AWS_BUCKET_NAME", None)

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request sdfsdf for {}".format(self.path).encode('utf-8'))
        self.wfile.write("<br>===================<br>".encode('utf-8'))
        # contents of the s3 bucket
        import boto3
        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket(DEFAULT_BUCKET)
        self.wfile.write("Files on the s3 Bucket<br>".encode('utf-8'))
        self.wfile.write("===================<br>".encode('utf-8'))
        for my_bucket_object in my_bucket.objects.all():
            print(my_bucket_object)

            data = str(my_bucket_object.key)
            self.wfile.write(data.encode('utf-8'))
            self.wfile.write("<br>----------------------------------<br>".encode('utf-8'))



    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
