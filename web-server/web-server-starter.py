import argparse
import sys
import itertools
import socket
from socket import socket as Socket

# A simple web server
def main():

    # Command line arguments. Use a port > 1024 by default so that we can run
    # without sudo, for use as a real server you need to use port 80.
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=2080, type=int,
                        help='Port to use')
    args = parser.parse_args()

    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind(('', args.port))
        server_socket.listen(1)

        print("Listening on port", args.port, "...")

        while True:
            
            with server_socket.accept()[0] as connection_socket:
                # This is a hackish way to make sure that we can receive and process multi
                # line requests.
                request=""
                received=connection_socket.recv(1024).decode('utf-8')
                request+=received 
                reply = http_handle(request)
                connection_socket.sendall(reply.encode('utf-8'))

            print("\n\nReceived request")
            print("======================")
            print(request.rstrip())
            print("======================")


            print("\n\nReplied with")
            print("======================")
            print(reply.rstrip())
            print("======================")



    return 0


def http_handle(request_string):
    """Given a http requst return a response

    Both request and response are unicode strings with platform standard
    line endings.
    """

    # request line and Header lines
    # parse HTTP headers
    # split the string by line
    headers = request_string.split(sep='\r\n')

    # get the method, url, and version
    method, filename, version = headers[0].split()

    # define request
    request = [method, filename, version]
    
    # gets rid of the request line
    headers.pop(0)
    
    # initialize dictionary
    dictionary = {}

    # loops through all the header lines
    for line in headers:
        if line.strip() == '':
            continue
        key, value = line.split( sep = ':', maxsplit=1)
        dictionary[key.strip()] = value.strip()


    # if method is compliant, but not implemented, we need to respond with a correct HTTP response
    # function: checkMethod
    checkMethod(method)

    # if the version is not compliant, we need to respond with a correct HTTP response
    # function: checkVersion
    checkVersion(version)

    # check if bad format
    # function: checkFormat
    checkFormat(request)
    
    # rename the url
    if filename == '/':
        filename = '/index.html'
        
    # check to make sure method, url, and version are all compliant
    # if method is a GET and url is "/" or "/index.html" and correct HTTP version,
    # we need to respond with 200 OK and some HTML        
    if method == 'GET' and version == 'HTTP/1.1' and (filename == '/' or filename == '/index.html'):
             
        # get the contents of the file
        try: 
            data = 'HTTP/1.1 200 OK\r\n'
            data+= 'Connection: keep-alive\r\n'
            data+= 'Content-Type: text/html; encoding=utf-8\r\n'
            file = open('index.html', 'r')
            # send data per line
            for line in file.readlines():
                data+=line
            file.close()
            data+="\r\n\r\n"

            # check if 404 not found error
            if "favicon" in request_string:
                data = "HTTP/1.1 404 Not Found\r\n\r\n"

            # return response
            return data

        # if file does not exist, return error
        except FileNotFoundError:

            return 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
    

        
    raise NotImplementedError

    pass


def checkFormat(req):
    # define our compliant methods
    compliantMethods = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT']
    filenames = ['/', '/index.html']
    version = ['HTTP/1.1']

    if req[0] not in compliantMethods and req[1] not in filenames and req[2] not in version:
        return 'HTTP/1.1 400 BAD REQUEST\n\nMalformed Syntax'
    
def checkVersion(vers):
    # define our compliant versions
    compliantVersions = ['HTTP/1.1']

    # check if version compliant
    if vers not in compliantVersions:
        return 'HTTP/1.1 505 VERSION NOT SUPPORTED\n\nHTTP Version Not Supported'
    

 
def checkMethod(inputMethod):
    # define our compliant methods
    compliantMethods = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT']
        
    # define our implemented methods
    implementedMethods = ['GET']

    # check if method comliant but not implemented
    if inputMethod in compliantMethods and inputMethod not in implementedMethods:     
        return 'HTTP/1.1 501 NOT IMPLEMENTED\n\nMethod Not Implemented'

    
if __name__ == "__main__":
    sys.exit(main())
