from settings import *
from image_handler import ImageHandler as ih

class NoiseServer(ih):
    def __init__(self, fake_server_port, real_server_port, block_size=BODY_SIZE):
        super().__init__(block_size, 'NoiseServer')
        # Получаем изображение от клиента
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_socket.bind((HOST, fake_server_port))
        self.recv_socket.listen()
        self.fake_server_port = fake_server_port

        # Отправляем изображение на сервер
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.real_server_port = real_server_port

    def run(self):
        # Открываем сокет
        with self.recv_socket as s:
            self.log(f'Accepting {self.fake_server_port}')
            conn, addr = s.accept()
            self.log('Connected. Sending image.')
            # Получаем изображение
            image = self.recv_image(conn)
        # Добавляем шум на изображение
        noise_image = self.add_noise(image)
        # Отправляем иходное и испорченное изображения на конечный сервер
        with self.send_socket as s:
            s.connect((HOST, self.real_server_port))
            self.send_image(image, s)
            self.send_image(noise_image, s)

    def add_noise(self, img):
        img = img.copy()
        h, w, _ = img.shape
        for y in range(h):
            for x in range(w):
                if random() > 0.9:
                    img[y, x] = int(random() > 0.5) * 255
        return img
