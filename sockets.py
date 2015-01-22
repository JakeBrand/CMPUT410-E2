# Copyright 2015 Jake Brand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# run: python sockets.py
# try: telnet localhost 1234 (on another terminal)
# type c to close connection
# use Ctrl-c as keyboard interrupt to kill the program
# Format adopted from
# http://www.binarytides.com/python-socket-server-code-example/

import socket
import sys  # for exiting
from thread import *  # for creating a thread

if __name__ == "__main__":

    # Function for handling connections. This will be used to create threads
    def handleConnection(connection):

        # inf. loop so that function do not terminate and thread doesnt end
        while 1:

            # Receiving message from client and strip off new line
            connection.sendall("Enter a string and I will add my name. " +
                               "enter c alone to close connection\r\n")
            message = str(connection.recv(4096))
            message = message.strip('\r\n')
            if (message == "c"):
                print("Closed connection")
                break
            reply = message + ' Jake\r\n'
            # Reply to client
            connection.sendall(reply)

        # close connection on this thread
        connection.close()

    # Create a new INET, STREAMing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Did not seem useful at all
    # host = "www.ualberta.ca"
    # port = 80

    # Bind socket to local host and port 1212
    try:
        s.bind(('localhost', 1234))
    # Bind caused socket exception. Print it and exit()
    except socket.error as msg:
        print 'Failed to create socket'
        print 'Code: ' + str(msg[0]) + ' Message: ' + msg[1]
        sys.exit()

    # None of this seemed necesary...
    # Get remote ip information
    # try:
    #     remote_ip = socket.gethostbyname(host)
    # except socket.gaierror:
    #     print("Host name could not be resolved")
    #     sys.exit()
    # print("IP: " + remote_ip)

    # create get message
    # mes = 'GET / HTTP/1.1\r\n\r\n'
    # try:
    #     s.sendall(mes.encode("UTF8"))
    # except socket.error:
    #     print("Send failed")
    #     sys.exit()

    # queue up as many as 5 connect requests
    s.listen(5)

    # accept connections from outside
    while 1:
        # goes (back to) accept more connections
        (clientSocket, address) = s.accept()
        print 'Connected with ' + address[0] + ':' + str(address[1])
        # start a new thread to handle communication for the connection
        start_new_thread(handleConnection, (clientSocket,))

    # close socket
    s.close()
