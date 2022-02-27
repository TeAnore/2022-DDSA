from settings import *
from image_handler import ImageHandler as ih

class Client(ih):
    def __init__(self, server_port, image, block_size=BODY_SIZE):
        super().__init__(block_size, 'Client')
        self.port = server_port
        self.image = image
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def run(self):
        # После старта подключаемся к серверу по порту и передаём изображение в сокет сервева
        with self.socket as s:
            self.log(f'Connecting to server with port {self.port}')
            s.connect((HOST, self.port))
            self.log('Connected. Sending image.')
            self.send_image(self.image, self.socket)

