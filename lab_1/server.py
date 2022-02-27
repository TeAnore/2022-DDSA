import socket
import cv2
import numpy as np
import settings as st
from image_networker import ImageNetworker as im

class Server(im):
    def __init__(self, server_port, block_size=1024, recv_noise=True, use_denoising=True):
        super().__init__(block_size, 'Server')
        self.port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((st.HOST, server_port))
        self.socket.listen()
        self.recv_noise = recv_noise
        self.use_denoising = use_denoising
    
    def run(self):
        with self.socket as s:
            self.log(f'Accepting {self.port}')
            conn, addr = s.accept()
            self.log('Connected. Receiving image.')
            self.image = self.recv_image(conn)
            # Make a placeholder for noise image in case it was not received
            self.noise_image = self.image
            if self.recv_noise:
                self.noise_image = self.recv_image(conn)

        self.denoised_image = self.noise_image
        if self.use_denoising:
            self.denoised_image = self.denoise(self.noise_image)

        self.log('Testing on denoised image')
        self.perform_test(self.denoised_image)
        self.log('Testing on noise image')
        self.perform_test(self.noise_image)

        img_name = 'noised.jpg'
        cv2.imwrite("data/" + img_name, self.noise_image)
        self.log(f'Saved: /data/{img_name}')

        img_name = 'denoised.jpg'
        cv2.imwrite("data/" + img_name, self.denoised_image)
        self.log(f'Saved: /data/{img_name}')

    def perform_test(self, noise_image):
        diff = (np.abs(self.image - noise_image) < 20).mean()
        self.log('Percentage of unaffected pixels:', diff)
        diff = np.abs(self.image - noise_image).astype('float32').mean()
        self.log('Mean absolute difference:', diff)
        diff = np.square((self.image - noise_image).astype('float32')).mean()
        self.log('Square difference:', diff)

    def denoise(self, img):
        return cv2.medianBlur(img, ksize=5)
