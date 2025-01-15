import socket
import threading
import os

from settings import Settings


settings = Settings()
clients = {}  # Dictionary to store connected clients
private_chats = {}  # Dictionary to store private chat sessions

LOGS_DIR = "chat_logs" # Directory to store chat logs
os.makedirs(LOGS_DIR, exist_ok=True) # Create the directory if it doesn't exist

# Function to save messages to a file
def save_message_to_file(filename, message):
    with open(os.path.join(LOGS_DIR, filename), "a", encoding="utf-8") as file:
        file.write(message + "\n")

# Function to send a private message
def send_private_message(sender, recipient, message):
    if recipient in clients:
        log_filename = f"chat_between_{min(sender, recipient)}_and_{max(sender, recipient)}.txt"
        try:
            # Save the message to the file
            save_message_to_file(log_filename, f"[{sender}]: {message}")
            # Send the message to the recipient
            clients[recipient].send(f"[{sender}]: \033[34m{message}\033[0m".encode('utf-8'))
        except:
            print(f"Error sending message to {recipient}")
    else:
        clients[sender].send(f"\n{recipient} is not connected.".encode('utf-8'))

# Function to handle each client
def handle_client(client_socket, client_address):
    username = client_socket.recv(1024).decode('utf-8')

    clients[username] = client_socket
    private_chats[username] = None  # No private chat at the start

    print(f"{username} connected from {client_address}")
    client_socket.send("Welcome to the chat server!\nThe user list will update automatically.\n".encode('utf-8'))

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')

            # Server commands
            if message.startswith("/start_chat"):
                parts = message.split(" ", 1)
                if len(parts) == 2 and parts[1] in clients:
                    recipient = parts[1]
                    private_chats[username] = recipient
                    private_chats[recipient] = username
                    client_socket.send(f"\nYou are now in a private chat with {recipient}\n".encode('utf-8'))
                    clients[recipient].send(f"{username} started a private chat with you.\n".encode('utf-8'))
                else:
                    client_socket.send("\nUser not found.\n".encode('utf-8'))

            elif message.startswith("/end_chat"):
                if private_chats.get(username):
                    recipient = private_chats[username]
                    private_chats[username] = None
                    private_chats[recipient] = None

                    log_filename = f"chat_between_{min(username, recipient)}_and_{max(username, recipient)}.txt"
                    save_message_to_file(log_filename, f"--- Chat ended between {username} and {recipient} ---")

                    client_socket.send("\nYou have exited the private chat.".encode('utf-8'))
                    clients[recipient].send(f"{username} has exited the private chat.".encode('utf-8'))
                else:
                    client_socket.send("\nYou are not in a private chat.".encode('utf-8'))

            # Private chat mode
            elif private_chats[username]:
                recipient = private_chats[username]
                send_private_message(username, recipient, message)

            else:
                client_socket.send("\nError: Unknown command.".encode('utf-8'))

        except:
            print(f"\n{username} disconnected")
            del clients[username]
            private_chats.pop(username, None)
            client_socket.close()
            break

# Function to start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((settings.config("HOST"), settings.config("PORT")))
    server_socket.listen(5)

    print(f"Server listening on {settings.config('HOST')}:{settings.config('PORT')}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Got a connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == '__main__':
    start_server()
