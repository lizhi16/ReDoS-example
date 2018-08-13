# -*- coding: utf-8 -*- 
import sys
import socket as so
import threading as th
 
ADDR = ('0.0.0.0', 8000)
static_root = './static'
handler_root = './handler'
 
 
class HTTPServer(object):
    def __init__(self, addr):
        self.sockfd = so.socket()
        self.sockfd.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR, 1)
        self.sockfd.bind(addr)
        print("Address is %s\n" % str(addr))
        self.sockfd.listen(100)
        self.serverName = '127.0.0.1'
        self.serverPort = 8000
 
    def serverForever(self):
        while True:
            #Don't use itself.connfd, because it will be reuse when mutiple requests arrived
            connfd, self.clientAddr = self.sockfd.accept()
            clientThread = th.Thread(target=self.handleRequest,args=(connfd,))
            clientThread.start()
 
    def setApp(self, application):
        self.application = application
 
    def handleRequest(self,connfd):
        self.recvData = connfd.recv(2048)
        requestHanders = self.recvData.splitlines()

        #print (requestHanders)
 
        getRequest = str(requestHanders[0]).split(' ')[1]

        if getRequest[-5:] == '/send':
            length = len(requestHanders)
            poststr = str(requestHanders[length-1]).split('\'')[1].split('=')[1]

            print ("This is poststr %s\n" % poststr)
         
            env = {}
            bodyContent = self.application(env, self.startResponse, poststr)
            response = 'HTTP/1.1 {}\r\n'.format(self.header_set[0])
            for header in self.header_set[1:]:
                response += '{0}:{1}\r\n'.format(*header)
            response += '\r\n'
            response += bodyContent
            connfd.send(response.encode())
        else:
            if getRequest == '/':
                getFilename = static_root + '/index.html'
            else:
                getFilename = static_root + getRequest
            try:
                f = open(getFilename)
            except:
                responseHeaders = 'HTTP/1.1 404 not found\r\n'
                responseHeaders += '\r\n'
                responseBody = '====sorry,file not find===='
            else:
                responseHeaders = 'HTTP/1.1 200 OK\r\n'
                responseHeaders += '\r\n'
                responseBody = f.read()
            finally:
                response = responseHeaders + responseBody
                connfd.send(response.encode())
        connfd.close()
        return
 
    def startResponse(self, status, response_handers):
        serverHeaders = [
            ('Date', '2018-5-21'),
            ('Server', 'HTTPServer 1.0'),
            ]
        self.header_set = [
            status,
            response_handers + serverHeaders
            ]
 
 
def main():
    # python3 HttpServer.py module app
    if len(sys.argv) < 3:
        sys.exit('please choose')
    sys.path.insert(0, handler_root)
    m = __import__(sys.argv[1])
    application = getattr(m, sys.argv[2])
 
    httpd = HTTPServer(ADDR)
    httpd.setApp(application)
    print('Serving HTTP on port 8000')
    httpd.serverForever()
 
 
if __name__ == '__main__':
    main()

