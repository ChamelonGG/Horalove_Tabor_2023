#pyright: ignore[reportShadowedImports]
import board
import wifi, time
from adafruit_httpserver import Server, Request, Response, POST, GET, JSONResponse
import socketpool
# Connect to Wi-Fi network
WIFI_SSID = 'TP-Link_Archer2300AC'
WIFI_PASSWORD = '67233182'

print("Connecting to Wi-Fi...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print("Connected!")


# Define response HTML

# Create an HTTP server
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static")
detonationTime = time.monotonic_ns()+150*1000000000 # 1minute
# Define a route for the root path
def stoms(seconds):
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i" % (minutes, seconds)
@server.route("/")
def base(request: Request):
    #  serve the HTML f string
    #  with content type text/html
    with open("./static/index.html") as fs:
        return Response(request, f"{fs.read()}", content_type='text/html')
@server.route("/bombData", [GET], append_slash=True)
def base(request: Request):
    data = [{"timeLeft": f"{stoms(round((detonationTime-time.monotonic_ns())/1000000000))}", "strikes":"_-_-_-_"}]
    if(detonationTime-time.monotonic_ns())/1000000000 <= 0:
        data = [{"timeLeft": f"--:--", "strikes":"x-x-x-x"}]
    #  serve the HTML f string
    #  with content type text/html
    return JSONResponse(request, data)
# Start the server
server.start(str(wifi.radio.ipv4_address))
print("Listening on http://%s:80" % wifi.radio.ipv4_address)

print("Server is up and running.")

while True:
    server.poll()
server.stop()

print("Server stopped.")
