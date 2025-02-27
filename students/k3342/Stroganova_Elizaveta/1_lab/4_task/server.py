import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = {}


def handle_client(client_socket):
    try:

        username = client_socket.recv(1024).decode().strip()
        clients[client_socket] = username
        print(f"{username} подключился!")

        broadcast(f"🎉 {username} присоединился к чату!", client_socket)

        while True:
            message = client_socket.recv(1024).decode().strip()
            if message.lower() == "/exit":
                break

            print(f"[{username}]: {message}")
            broadcast(f"[{username}]: {message}", client_socket)

    except ConnectionResetError:
        pass
    finally:
        username = clients.pop(client_socket, "Неизвестный пользователь")
        print(f"{username} отключился.")
        broadcast(f"❌ {username} вышел из чата.", client_socket)
        client_socket.close()


def broadcast(message, sender_socket=None):
    for client in list(clients.keys()):
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                clients.pop(client, None)
                client.close()


print(f"Сервер запущен на {HOST}:{PORT} и ожидает клиентов...")

while True:
    client_socket, _ = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
