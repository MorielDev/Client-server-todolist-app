import socket
import threading

HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}...")

# Predefined responses for the server
RESPONSES = {
    "hi": "Hello! How can I help you?",
    "hello": "Hello! How can I help you?",
    "how are you": "I'm just a server, but I'm doing great! How about you?",
    "what's your name": "I'm the Chat Server!",
    "exit": "Goodbye! Have a great day!",
}

def get_server_response(message):
    """Generate a response based on the client's message."""
    message = message.lower().strip()
    for key in RESPONSES:
        if key in message:  # Check if the key is a substring of the message
            return RESPONSES[key]
    return "I'm not sure how to respond to that. Can you rephrase?"

def handle_client(client_socket, addr):
    print(f"New connection from {addr}")

    def receive():
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    print(f"Connection closed by {addr}")
                    break
                print(f"Client [{addr}]: {message}")
                if message.lower().strip() == 'exit':
                    break
                # Generate a response
                response = get_server_response(message)
                client_socket.send(response.encode())
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        client_socket.close()

    # Start a thread for receiving messages
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    receive_thread.join()

    print(f"Connection with {addr} closed.")

while True:
    client_socket, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()