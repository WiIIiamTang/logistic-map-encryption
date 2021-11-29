from .EncryptDecrypt import ImageEncryptDecrypter
from PIL import Image
import numpy as np

class SimpleStream(ImageEncryptDecrypter):
    def __init__(self, name: str='SimpleStreamEncrypter'):
        super().__init__(name)
    
    def encrypt_action(self, image: Image, key=None) -> tuple:
        size = image.size
        if isinstance(key, np.ndarray):
            key = key
        else:
            key = self.keygen(image, size)
        pixels = image.load()
        for i in range(size[0]):
            for j in range(size[1]):
                pixels[i, j] = tuple(o^key[i][j][p] for p,o in enumerate(pixels[i, j]))
        
        return image, key

    def decrypt(self, key, image: Image) -> Image:
        return self.encrypt_action(image=image, key=key)[0]

    def keygen(self, image: Image, size: tuple):
        return np.random.randint(low=0, high=256, size=(size[0], size[0], self.pixel_size))
    
    