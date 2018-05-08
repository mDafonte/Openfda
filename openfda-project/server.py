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
        conn = http.client.HTTPSConnection("api.fda.gov")
        message="<ul>"
        if self.path == "/":
            with open("search2.html","r")as f:
                message=f.read()
        elif "searchDrug" in self.path:
            drug=self.path.split("&")[0].split("=")[1]
            limit=self.path.split("&")[1].split("=")[1]
            url = "/drug/label.json?search=active_ingredient:" + drug + "&" + "limit=" + limit
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            info_bruto = r1.read().decode("utf-8")
            conn.close()
            info_lista = json.loads(info_bruto)
            for i in range(len(info_lista["results"])):
                message=message+"<li>"+info_lista["results"][i][0]+"</li>"
                message = message + "\n\t<li>" + info_lista["results"][i]["active_ingredient"][0] + "</li>"
            message=message+"\n</ul>"
        elif "searchCompany" in self.path:
            company=self.path.split("&")[0].split("=")[1]
            limit=self.path.split("&")[1].split("=")[1]
            url = "/drug/label.json?search=manufacturer_name:" + company + "&" + "limit=" + limit
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            info_bruto = r1.read().decode("utf-8")
            conn.close()
            info_lista = json.loads(info_bruto)
            for i in range(len(info_lista["results"])):
                message= message+"\n\t<li>"+info_lista["results"][i]["openfda"]["manufacturer_name"][0]+"</li>"
            message = message + "\n</ul>"
        elif "listDrug" in self.path:
            n=self.path.split("?")[1].split("=")[1]
            url = "/drug/label.json?limit=" + n
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            info_bruto = r1.read().decode("utf-8")
            conn.close()
            info_lista = json.loads(info_bruto)
            for i in range(len(info_lista["results"])):
                try:
                    message=message+"\n\t<li>"+info_lista["results"][i]["openfda"]["brand_name"][0]+"</li>"
                except KeyError:
                    message=message+"\n\t<li>Unknown</li>"
            message = message + "\n</ul>"
        elif "listCompanies"in self.path:
            n=self.path.split("?")[1].split("=")[1]
            url = "/drug/label.json?limit=" + n
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            info_bruto = r1.read().decode("utf-8")
            conn.close()
            info_lista = json.loads(info_bruto)
            for i in range(len(info_lista["results"])):
                try:
                    message=message+"\n\t<li>"+info_lista["results"][i]["openfda"]["manufacturer_name"][0]+"</li>"
                except KeyError:
                    message=message+"\n\t<li>Unknown</li>"
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        return

Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()