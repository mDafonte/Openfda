import http.server
import json
import socketserver

PORT = 8000

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        headers = {'User-Agent': 'http-client'}
        drugs_id=[]
        message=""
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?limit=10", None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        drugs_raw = r1.read().decode("utf-8")
        drugs=json.loads(drugs_raw)
        conn.close()
        for i in range(len(drugs['results'])):
            drugs_id.append(drugs["results"][i]["id"])
        for elem in drugs_id:
            message=message +"<ol>"+elem+"</ol>"
        self.send_response(200)
        with open("drugs.html","w")as f:
            f.write(message)
        with open("drugs.html","r") as f:
            patata=f.read()
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = patata
        self.wfile.write(bytes(message, "utf8"))
        return

Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

# https://github.com/joshmaker/simple-python-webserver/blob/master/server.py