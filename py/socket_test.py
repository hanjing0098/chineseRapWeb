import socket
import sys
host = "10.125.13.5"
port = 8080 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
