import http.server
import json
import socketserver
socketserver.TCPServer.allow_reuse_adress = True
IP="localhost"
PORT = 8000

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        headers = {'User-Agent': 'http-client'}
        self.send_response(200)
        if self.path == "/":
            with open("search2.html","r")as f:
                message=f.read()
        elif "search" in self.path:
            conn = http.client.HTTPSConnection("api.fda.gov")
            drug=self.path.split("&")[0].split("=")[1]
            limit=self.path.split("&")[1].split("=")[1]
            url = "/drug/label.json?search=active_ingredient:" + drug + "&" + "limit=" + limit
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            info_bruto = r1.read().decode("utf-8")
            conn.close()
            message = json.loads(info_bruto)
            message = str(info_bruto)
        self.wfile.write(bytes(message, "utf8"))
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        return

Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()