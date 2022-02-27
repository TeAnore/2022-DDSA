import socket
import cv2
from random import random
import numpy as np

# Базовые настройки приложения сокетов серверов
HOST = '127.0.0.1'
NOISY_SERVER_PORT = 65003
NORMAL_SERVER_PORT = 65004
BODY_SIZE = np.uint32(2048)
