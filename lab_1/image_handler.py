from settings import *
from multiprocessing.dummy import Process

class ImageHandler(Process):
    """
        Содержит основные процедуры обработки изображений
    """
    def __init__(self, block_size=BODY_SIZE, name='ImageHandler'):
        super().__init__()
        self.block_size = block_size
        self.name = name

    def log(self, *args):
        print(f'{self.name} :', *args)

    # Методы отправки изображения
    def send_image(self, image, socket):
        # Вычисляем мета данные изображения
        n_bytes = self.send_image_meta(image, socket)
        n_iters = n_bytes // self.block_size
        n_remains = n_bytes - n_iters * self.block_size
        im_bytes = image.tobytes()
        for i in range(n_iters):
            block = im_bytes[self.block_size * i: (i + 1) * self.block_size]
            assert socket.sendall(block) is None, f'Could not send image byte block i={i}'

        if n_remains > 0:
            block = im_bytes[-n_remains:]
            assert socket.sendall(block) is None, f'Could not send remaining byte block'

        self.log('Image is sent.')

    def send_image_meta(self, image, socket):
        h, w, _ = image.shape
        n_bytes = h * w * 3  # Так как RGB это 3 канала
        # Отправляем мета данные
        # 1. Размер
        assert self.send_int(n_bytes, socket) is None, 'Could not send n_bytes'
        # 2. Высота
        assert self.send_int(h, socket) is None, 'Could not send height'
        # 3. Ширина
        assert self.send_int(w, socket) is None, 'Could not send width'
        return n_bytes

    def send_int(self, number, socket):
        _bytes = number.to_bytes(length=4, byteorder='big')
        return socket.sendall(_bytes)

    # Методы получения изображения
    def recv_image(self, conn):
        n_bytes, h, w = self.recv_image_meta(conn)
        n_iters = n_bytes // self.block_size
        n_remains = n_bytes - n_iters * self.block_size
        im_bytes = []
        n_received = 0
        while True:
            block = conn.recv(self.block_size)
            im_bytes.append(block)
            n_received += len(block)

            if n_received == n_bytes:
                break

        im_bytes = b''.join(im_bytes)
        image = np.frombuffer(im_bytes, dtype='uint8')
        image = image.reshape(h, w, 3)

        self.log(f'Received image with size={h, w}.')
        return image

    def recv_image_meta(self, conn):
        # Получаем мета данные
        # 1. Размер
        n_bytes = self.recv_int(conn)
        # 2. Высота
        h = self.recv_int(conn)
        # 3. Ширина
        w = self.recv_int(conn)
        return n_bytes, h, w

    def recv_int(self, conn):
        _bytes = conn.recv(4)
        return int.from_bytes(_bytes, byteorder='big')
