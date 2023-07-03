from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

hostName = "localhost"
serverPort = 8080

REQUESTS_TOTAL = Counter('http_request_total', 'Total number of http requests')
REQUEST_DURATION = Histogram('http_request_duration_seconds',
                             'Histogram for the duration in seconds.',
                             buckets=(0.1, 0.2, 0.5, 1.0, 2.0))


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-Type', CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(generate_latest())
        else:
            with REQUEST_DURATION.time():
                REQUESTS_TOTAL.inc()
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
                self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
                self.wfile.write(bytes("<body>", "utf-8"))
                self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
                self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
