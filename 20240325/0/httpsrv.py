import sys
import socket
from http.server import test, SimpleHTTPRequestHandler
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
s.close()


PORT = sys.argv[1] if len(sys.argv) > 1 else "8000"
print(HOST)
test(SimpleHTTPRequestHandler, port=int(PORT))