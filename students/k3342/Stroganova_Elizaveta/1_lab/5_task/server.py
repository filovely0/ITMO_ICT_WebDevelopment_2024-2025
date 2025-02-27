import socket
import threading
from urllib.parse import urlparse, parse_qs

# Храним оценки в виде словаря { "Математика": [5, 4], "Физика": [3] }
grades = {}

def handle_request(client_socket):
    """Обрабатывает HTTP-запросы от клиента"""
    request = client_socket.recv(1024).decode()
    if not request:
        client_socket.close()
        return

    # Парсим первую строку запроса (например, "POST / HTTP/1.1")
    first_line = request.split("\n")[0]
    method, path, _ = first_line.split()

    if method == "GET":
        # Генерируем HTML-страницу с оценками
        response = generate_html()
    elif method == "POST":
        # Получаем данные из запроса
        body = request.split("\r\n\r\n")[-1]
        data = parse_qs(body)
        subject = data.get("subject", [""])[0]
        grade = data.get("grade", [""])[0]

        # Добавляем оценку в журнал
        if subject and grade.isdigit():
            grade = int(grade)
            if subject in grades:
                grades[subject].append(grade)
            else:
                grades[subject] = [grade]

        response = generate_html()

    else:
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Allowed"

    client_socket.sendall(response.encode())
    client_socket.close()

def generate_html():
    """Генерирует HTML-страницу с оценками"""
    html = """<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Журнал оценок</title>
    </head>
    <body>
        <h1>Журнал оценок</h1>
    """
    if grades:
        html += "<ul>"
        for subject, marks in grades.items():
            html += f"<li><strong>{subject}</strong>: {', '.join(map(str, marks))}</li>"
        html += "</ul>"
    else:
        html += "<p>Пока нет оценок.</p>"

    # Форма для добавления новой оценки
    html += """
        <h2>Добавить оценку</h2>
        <form method="POST">
            Дисциплина: <input type="text" name="subject" required><br>
            Оценка: <input type="number" name="grade" required><br>
            <button type="submit">Добавить</button>
        </form>
    </body></html>
    """

    # Добавляем заголовок charset=utf-8
    return f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{html}"


def start_server():
    """Запускает сервер"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 8080))
    server_socket.listen(5)
    print("🚀 Сервер запущен на http://127.0.0.1:8080")

    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_request, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
