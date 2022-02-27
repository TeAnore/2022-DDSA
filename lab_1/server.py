from settings import *
from image_handler import ImageHandler as ih

class Server(ih):
    def __init__(self, server_port, block_size=BODY_SIZE, recv_noise=True, use_denoising=True):
        super().__init__(block_size, 'Server')
        self.port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, server_port))
        self.socket.listen()
        self.recv_noise = recv_noise
        self.use_denoising = use_denoising
    
    def run(self):
        # Поднимаем сокет для ожидания подключения (Листенер)
        with self.socket as s:
            self.log(f'Accepting {self.port}')
            conn, addr = s.accept()
            self.log('Connected. Receiving image.')
            # Получаем исходное изображение
            self.image = self.recv_image(conn)
            # Получаем шумное изображение
            self.noise_image = self.recv_image(conn)

        # Чиним изображение
        self.denoised_image = self.noise_image
        if self.use_denoising:
            self.denoised_image = self.denoise(self.noise_image)

        # Вычисляем потери с шумом
        self.log('Оценка качества noise image')
        self.perform_test(self.noise_image)
        # Сохраняем для визуализации
        img_name = 'noised.jpg'
        cv2.imwrite("data/" + img_name, self.noise_image[..., ::1])
        self.log('Сохранено: lab_1/data/', img_name)
        # Вычисляем потери после восстановления
        self.log('Оценка качества denoised image')
        self.perform_test(self.denoised_image)
        # Сохраняем для визуализации
        img_name = 'denoised.jpg'
        cv2.imwrite("data/" + img_name, self.denoised_image[..., ::1])
        self.log('Сохранено: lab_1/data/', img_name)

    def perform_test(self, noise_image):
        # Вычисляем количество нетронутых пикселей
        diff = (np.abs(self.image - noise_image) < 20).mean()
        self.log('Вычисляем количество нетронутых пикселей:', diff * 100)
        # Вычисляем среднее отклонение каждого пикселя
        diff = np.abs(self.image - noise_image).astype('float32').mean()
        self.log('Вычисляем среднее отклонение каждого пикселя:', diff)
        #Вычисляем среднеквадратичное отклонение:
        diff = np.square((self.image - noise_image).astype('float32')).mean()
        self.log('Вычисляем среднеквадратичное отклонение:', diff)

    def denoise(self, img):
        return cv2.medianBlur(img, ksize=5)
