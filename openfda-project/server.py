import http.server
import json
import socketserver
import http.client
socketserver.TCPServer.allow_reuse_adress = True
IP="localhost"
PORT = 8000
class OpenFDAHTML():
    def texto(self,lista):
        movida=""
        for elem in lista:
            movida=movida+"\n\t<li>" + elem + "</li>"
        message="<!doctype html>" + "\n" + "<html>" + "\n" + "<body>" + "\n" "<ul>" + "\n"+movida+"</ul>" + "\n" + "</body>" + "\n" + "</html>"
        with open("text.html","w")as f:
            f.write(message)
class OpenFDAClient():
    def urldrug(self,url):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", url, None, headers)
        r1 = conn.getresponse()
        info_bruto = r1.read().decode("utf-8")
        info_lista=json.loads(info_bruto)
        conn.close()
        return info_lista
class OpenFDAParser():
    def lol(self,info_lista,plus):
        list=[]
        for i in range(len(info_lista["results"])):
            list.append(info_lista["results"][i][plus]
        return list
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        list=[]
        if self.path == "/":
            self.send_response(200)
            with open("search2.html","r")as f:
                message=f.read()
            with open("text.html","w")as f:
                f.write(message)

        elif "searchDrug" in self.path:
            self.send_response(200)
            drug=self.path.split("&")[0].split("=")[1]
            limit=self.path.split("&")[1].split("=")[1]
            url = "/drug/label.json?search=active_ingredient:" + drug + "&" + "limit=" + limit
            info_lista= OpenFDAClient.urldrug(self,url)
            abba=["active_ingredient"][0]

            OpenFDAHTML.texto(self,list)

        elif "searchCompany" in self.path:
            self.send_response(200)
            company=self.path.split("&")[0].split("=")[1]
            limit=self.path.split("&")[1].split("=")[1]
            url = "/drug/label.json?search=manufacturer_name:" + company + "&" + "limit=" + limit
            info_lista = OpenFDAClient.urldrug(self, url)
            for i in range(len(info_lista["results"])):
                list.append(info_lista["results"][i]["openfda"]["manufacturer_name"][0])
            OpenFDAHTML.texto(self, list)

        elif "listDrugs" in self.path:
            self.send_response(200)
            n=self.path.split("?")[1].split("=")[1]
            url = "/drug/label.json?limit=" + n
            info_lista = OpenFDAClient.urldrug(self, url)

            for i in range(len(info_lista["results"])):
                try:
                    list.append(info_lista["results"][i]["openfda"]["brand_name"][0])
                except KeyError:
                    list.append("Unknown")
            OpenFDAHTML.texto(self, list)

        elif "listCompanies"in self.path:
            self.send_response(200)
            n=self.path.split("?")[1].split("=")[1]
            url = "/drug/label.json?limit=" + n
            info_lista = OpenFDAClient.urldrug(self, url)
            for i in range(len(info_lista["results"])):
                try:
                    list.append(info_lista["results"][i]["openfda"]["manufacturer_name"][0])
                except KeyError:
                    list.append("Unknown")
            OpenFDAHTML.texto(self, list)

        elif "listWarnings"in self.path:
            self.send_response(200)
            n = self.path.split("?")[1].split("=")[1]
            url = "/drug/label.json?limit=" + n
            info_lista = OpenFDAClient.urldrug(self, url)
            for i in range(len(info_lista["results"])):
                try:
                    list.append(info_lista["results"][i]["warnings"][0])
                except KeyError:
                    list.append("Unknown")
            OpenFDAHTML.texto(self, list)

        else:
            self.send_response(404)
            list.append("Error 404: Webpage not found")
            OpenFDAHTML.texto(self, list)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open("text.html","r")as f:
            file=f.read()
        self.wfile.write(bytes(file, "utf8"))
        return

Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()