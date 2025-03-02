
from server import Server
from time_utils import get_current_time
from wifi_connection import scan_wifi

my_server = Server()
server_socket = my_server.init_socket()


@my_server.get("/hello", app_type="application/json")
def hello():
  return "{\"message\":\"Hello, World!\"}"


@my_server.get("/about", app_type="application/json")
def about():
  return "{\"message\":\"This is a simple Python web server\"}"


@my_server.get("/time", app_type="application/json")
def time_get():
  return "{\"message\":\"Now - " + get_current_time() + "\"}"


@my_server.get("/")
def web_page():
  try:
    with open("index.html", "r") as f:
      return f.read()
  except OSError:
    return "404 Not Found"


@my_server.get("/name", app_type="application/json", paramm=["name"])
def web_name(params):
  print(f"Params - {params}")
  return "{\"message\":\"" + params[0] + "\"}"


@my_server.get("/wifi", app_type="application/json")
def hello_wifi():
  print("Scanning wifi..." + scan_wifi())
  return scan_wifi()


def server_handler():
  my_server.handle_client(server_socket)
