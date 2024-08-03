import argparse
import socket
import threading
from pathlib import Path

BUFFER_SIZE = 1024
ENCODING = "utf-8"

def response_with_content(content, content_type="text/plain", code=200):
    return f"HTTP/1.1 {code} OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n{content}"

def file_response(http_method, path, body, directory):
    file_path = Path(directory) / path.split('/')[-1]
    content_type = "application/octet-stream"
    if http_method == "POST":
        file_path.write_text(body)
        return response_with_content('', content_type, 201)
    elif file_path.is_file():
        return response_with_content(file_path.read_text(), content_type)

def response(http_method, path, user_agent, body, directory):
    if path[0:6] == "/files":
        response = file_response(http_method, path, body, directory)
        if response:
            return response
    elif path[0:5] == "/echo":
        random_string = '/'.join(path.split('/')[2:])
        return response_with_content(random_string)
    elif path[0:11] == "/user-agent":
        return response_with_content(user_agent)
    elif path == "/":
        return "HTTP/1.1 200 OK\r\n\r\n"

    return "HTTP/1.1 404 Not Found\r\n\r\n"

def parse_request(request):
    request_lines = request.split("\r\n")
    http_method, path, _ = request_lines[0].split(" ", 2)
    user_agent = None
    for line in request_lines:
        if line.startswith("User-Agent:"):
            user_agent = line.split(" ")[1]
            break
    body = request_lines[-1] if http_method == "POST" else None

    return http_method, path, user_agent, body

def handle_client(client_socket, address, directory):
    data = client_socket.recv(BUFFER_SIZE)
    request = data.decode(ENCODING)
    print(f"Request from {address}:\n{request}")

    http_method, path, user_agent, body = parse_request(request)

    client_socket.sendall(response(http_method, path, user_agent, body, directory).encode(ENCODING))
    client_socket.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str)
    args = parser.parse_args()

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen()

    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address, args.directory))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
    
    
    
      
# import socket
# from threading import Thread

# def main():
#   server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
#   server_socket.listen()
#   try
#   while True:
#     stream, _addr = server_socket.accept()
    
#     thread = Thread(target=route_handler, args=(stream, _addr))
#     thread.start()
    
#     except KeyboardInterrupt
#     print("Server")
#     finally:
#       server_socket.close()


#     def route_handler(stream):
#       while True:
#         req_data = stream.recv(40496).decode()
#         if not req_data:
#           return
        
#         req_lines = req_data.split("\r\n")
#         method, path, version = req_lines[0].split(" ")
#         user_agent = req_lines[2]
        
#         if path == "/":
#           http_res = "HTTP/1.1 200 0K\r\n\r\n"
#           stream.send(http_res.encode())
#         elif path.startswith("/echo/"):
#           echo_res = echo_handler(path)
#           stream.send(echo_res.encode())
#         elif path.startswith("/user-agent"):
#           ua_res = user_agent_handler(user_agent)
#           stream.send(ua_res.encode())
#         else:
#           http_not_found = "HTTP/1.1 404 NOT FOUND\r\n\r\n"
#           stream.send(http_not_found.encode())
          
#           stream.close()
          
#           def echo_handler(path):
#             echo_str = path.split("/echo/")[-1]
            
#             content_type = "Content-Type: text/plain"
#             content_len = f"Content-Length: {len(echo_str)}"
#             status_line = "HTTP/1.1 200 OK"
#             http_res = (
#               f"{status_line}\r\n{content_type}\r\n{content_len}\r\n\r\n{echo_str}\r\n"
#             )
            
#             return http_res
          
#           def user_agent_handler(user_agent):
#             print(f"HERE: {user_agent}")
#             _ua_header, ua = user_agent.split(": ")
            
#             content_type = "Content_Type: text/plain"
#             content_len = f"Content-length: {len(ua)}"
#             status_line = "HTTP/1.1 200 OK"
#             http_res = f"{status_line}\r\n{content_type}\r\n{content_len}\r\n\r\n{ua}\r\n\r\n"
            
#             return http_res
          
#           if __name__ == "__main__":
#             main()