
import http.server
import json
import socketserver
socketserver.TCPServer.allow_reuse_adress = True
PORT = 8000

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send respnse status code
        self.send_response(200)

        # Send Headers
        self.send_header("Content-type","text/html")
        self.end_headers()
        with open("search.html","r") as f:
            message= f.read()
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()