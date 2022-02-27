# Инициализация
from settings import *
from client import Client
from server import Server
from noise_server import NoiseServer

# Основной скрипт
if __name__ == '__main__' :
    # Считываем исходное изображение
    img_original = cv2.imread('data/original.png')
    # Создаём объект конечного сервера для обработки изображений
    server = Server(NORMAL_SERVER_PORT, use_denoising=True)
    server.start()
    # Создаём объект шумного сервера для обработки изображений
    noise_server = NoiseServer(NOISY_SERVER_PORT, NORMAL_SERVER_PORT)
    noise_server.start()
    # Создаём объект клиента
    client = Client(NOISY_SERVER_PORT, img_original)
    client.start()
