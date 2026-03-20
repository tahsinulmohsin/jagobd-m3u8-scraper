import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))
from index import handler
from http.server import HTTPServer
import threading
import requests
import time

server = HTTPServer(('localhost', 8081), handler)

def test_fetch():
    time.sleep(1)
    print("Fetching http://localhost:8081 ...")
    r = requests.get('http://localhost:8081')
    print("Response Code:", r.status_code)
    print("Headers:", r.headers)
    m3u8 = r.text
    print("Length of raw M3U8:", len(m3u8))
    print("Preview:\n", "\n".join(m3u8.split("\n")[:10]))
    os._exit(0)

threading.Thread(target=test_fetch).start()
print("Starting server on http://localhost:8081")
server.serve_forever()
