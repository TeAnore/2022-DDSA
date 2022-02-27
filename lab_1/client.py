import socket
import settings as st
from image_networker import ImageNetworker

class Client(ImageNetworker):
    def __init__(self, server_port, image, block_size=st.BODY_SIZE):
        super().__init__(block_size, 'Client')
        self.port = server_port
        self.image = image
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def run(self):
        with self.socket as s:
            self.log(f'Connecting to server with port {self.port}')
            s.connect((st.HOST, self.port))
            self.log('Connected. Sending image.')
            self.send_image(self.image, self.socket)

