# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from http.server import BaseHTTPRequestHandler, HTTPServer
import psutil
import json
import os
html = '<html><body><h3>Hello Alexander Yurevich</h3><img src="mashikhin.jpg"/></body></html>'

def cpu_temp():
    pt = psutil.cpu_percent()
    return pt
def disk_space():
    st = psutil.disk_usage(".")
    return st.free, st.total

def cpu_load() -> int:
    return int(psutil.cpu_percent())

def ram_usage() -> int:
    return int(psutil.virtual_memory().percent)


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        elif self.path.endswith(".jpg"):
            self.send_response(200)
            self.send_header('Content-type', 'image/jpg')
            self.end_headers()
            with open(os.curdir + os.sep + self.path, 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == "/status":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            health = {'CPUTemp':cpu_temp(),'CPULoad': cpu_load(), "DiskFree": disk_space()[0], "DiskTotal": disk_space()[1], "RAMUse": ram_usage()}
            self.wfile.write(json.dumps(health).encode('utf-8'))

        else:
            self.send_error(404, "Page Not Found {}".format(self.path))

def server_thread(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    port = 8000
    print("Starting server at port %d" % port)
    server_thread(port)
