
import socket

PORT = 8092
MAX_OPEN_REQUESTS = 5
import http.client
import json


def process_client(clientsocket):
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json", None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()
    print(repos_raw)
    repos = json.loads(repos_raw)
    web_contents = (
    "The id of the first repository is", repos['results'][0]['id'], "\n", "The purpose of the first repository is",
    repos['results'][0]['purpose'], "\n", "The manufacturer name of the first repository is",
    repos['results'][0]['openfda']['manufacturer_name'])

    print(clientsocket)
    jaja= clientsocket.recv(1024)

    web_headers = "HTTP/1.1 200"
    web_headers += "\n" + "Content-Type: text/html"
    web_headers += "\n" + "Content-Length: %i" % len(str.encode(web_contents))
    clientsocket.send(str.encode(web_headers + "\n\n" + web_contents))
    clientsocket.close()


# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
hostname = socket.gethostname()
hostname = "localhost"
# Let's use better the local interface name

try:
    serversocket.bind((hostname, PORT),)
    # become a server socket
    # MAX_OPEN_REQUESTS connect requests before refusing outside connections
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        # accept connections from outside
        print ("Waiting for connections at %s %i" % (hostname, PORT))
        (clientsocket, address) = serversocket.accept()
        # now do something with the clientsocket
        # in this case, we'll pretend this is a non threaded server
        process_client(clientsocket)

except socket.error as ex:
    print("Problemas using port %i. Do you have permission?" % PORT)
    print(ex)