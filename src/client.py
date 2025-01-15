import socket
import threading
from settings import Settings

settings = Settings()

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("\nConnection to the server lost.")
            client.close()
            break

# Connecting to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((settings.config("HOST"), settings.config("PORT")))

# Starting a thread to receive messages
threading.Thread(target=receive_messages, daemon=True).start()

# Entering username
username = input("Enter your username: ")
client.send(username.encode('utf-8'))
print("\n\033[1mInstructions:\033[0m\n start chat: \033[32m/start_chat \033[0m<\033[32muser_name\033[0m>\n end chat: \033[31m/end_chat\033[0m \n")

# Sending messages to the server
while True:
    message = input("")
    client.send(message.encode('utf-8'))

