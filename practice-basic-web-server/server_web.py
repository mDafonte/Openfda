# A basic web server using sockets


import socket

PORT = 8092
MAX_OPEN_REQUESTS = 5


def process_client(clientsocket):
    print(clientsocket)
    jaja= clientsocket.recv(1024)
    jajaja= str(jaja)
    if "GET /new" in  jajaja:
        with open("chocu2.html","r")as f:
            web_contents=f.read()
    else:
        with open("chocu1.html","r") as f:
            web_contents=f.read()
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