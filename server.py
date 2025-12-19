from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 80

server = HTTPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler)
print(f"Serving on port {PORT}")
server.serve_forever()
