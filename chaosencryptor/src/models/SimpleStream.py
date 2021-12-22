from .EncryptDecrypt import ImageEncryptDecrypter
from PIL import Image
import numpy as np

class SimpleStream(ImageEncryptDecrypter):
    def __init__(self, name: str='SimpleStreamEncrypter'):
        super().__init__(name)
    
    def encrypt_action(self, image: Image, key=None) -> tuple:
        size = image.size
        if not key:
            key = self.keygen(image, size)
        else:
            key = key

        keymap = self.create_keymap(key, size)
        pixels = image.load()

        for i in range(size[0]):
            for j in range(size[1]):
                pixels[i, j] = tuple(o^keymap[i][j][p] for p,o in enumerate(pixels[i, j]))
        
        return image, key
    
    def create_keymap(self, key: dict, size: tuple) -> any:
        np.random.seed(int(key.get('seed')))
        offset = key.get('offset')
        np.random.randint(0, 1, size=offset)
        return np.random.randint(low=0, high=256, size=(size[0], size[0], self.pixel_size))

    def decrypt(self, key: dict, image: Image) -> Image:
        return self.encrypt_action(image=image, key=key)[0]

    def keygen(self, image: Image, size: tuple):
        return {'seed': np.random.randint(1, 1000000), 'offset': np.random.randint(1, 1000000)}
    
    