import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

username = input("Введите ваше имя: ")
client_socket.send(username.encode())


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print("\n" + message)
        except:
            print("⚠️ Соединение с сервером потеряно.")
            break


thread = threading.Thread(target=receive_messages, daemon=True)
thread.start()

print("🔵 Вы подключились к чату! Введите сообщение и нажмите Enter (или /exit для выхода).")

while True:
    try:
        message = input()
        if message.lower() == "/exit":
            client_socket.send(message.encode())
            print("🔴 Вы вышли из чата.")
            client_socket.close()
            break
        client_socket.send(message.encode())
    except KeyboardInterrupt:
        print("\n🔴 Вы вышли из чата.")
        client_socket.send("/exit".encode())
        client_socket.close()
        break
