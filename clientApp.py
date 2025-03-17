import socket
import threading

HOST = '127.0.0.1'  # Server IP
PORT = 12345        # Server Port

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print(f"Connected to server at {HOST}:{PORT}")

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print("Server closed the connection.")
                break
            print(f"Server: {message}")
            if message.lower().strip() == 'exit':
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    client_socket.close()

def send():
    while True:
        try:
            message = input("You: ")
            client_socket.send(message.encode())
            if message.lower().strip() == 'exit':
                break
        except Exception as e:
            print(f"Error sending message: {e}")
            break
    client_socket.close()

# Start threads for sending and receiving
receive_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()

print("Disconnected from server.")