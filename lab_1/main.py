import cv2
import settings as st
from client import Client
from server import Server
from noise_server import NoiseServer

im_original = cv2.imread('data/original.png')
server = Server(st.NORMAL_SERVER_PORT, use_denoising=True)
server.start()
noise_server = NoiseServer(st.NOISY_SERVER_PORT, st.NORMAL_SERVER_PORT)
noise_server.start()
client = Client(st.NOISY_SERVER_PORT, im_original)
client.start()
