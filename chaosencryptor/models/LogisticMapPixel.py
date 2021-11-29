from PIL import Image
import numpy as np
import math
from tqdm import tqdm
from random import SystemRandom
from .EncryptDecrypt import ImageEncryptDecrypter


class LogisticMapPixel(ImageEncryptDecrypter):
    def __init__(self, name: str='LogisticMapPixelEncrypter', r_min=3.86, r_max=3.999999, offset_range: tuple=(0, 255)):
        super().__init__(name)
        self.sysrand = SystemRandom()
        self.r_min = r_min
        self.r_max = r_max
        self.offset_range = offset_range
    
    def _forward_l(self, x: float, n: int, r: float):
        directions = []
        offset = self.sysrand.randrange(self.offset_range[0], self.offset_range[1])
        x = (x + offset) / (255+self.offset_range[1]-self.offset_range[0])
        for _ in range(n):
            tmp = x
            x = r*x*(1-x)
            roots = np.roots([-1, 1, -x/r]).real[:]
            directions.insert(0, 0 if math.isclose(tmp, roots[0]) else 1)
        
        return x, n, r, directions, offset

    def _backward_l(self, x: float, n: int, r: float, directions: list):
        return self._backward_l(
            np.roots([-1, 1, -x/r]).real[directions.pop(0)],
            n-1,
            r,
            directions
        ) if n != 0 else x
    
    def encrypt_action(self, image: Image, key=None) -> tuple:
        size = image.size
        key = []
        pixels = image.load()
        for i in tqdm(range(size[0])):
            for j in range(size[1]):
                tmp = []
                for k in pixels[i, j]:
                    keypart = self._forward_l(k, self.sysrand.randrange(5, 15), (self.sysrand.random() * (self.r_max-self.r_min)) + self.r_min)
                    tmp.append(int(keypart[0]*255))
                    key.append(keypart)
                pixels[i, j] = tuple(tmp)

        return image, key

    def decrypt(self, key, image: Image) -> Image:
        size = image.size
        pixels = image.load()
        for i in range(size[0]):
            for j in range(size[1]):
                tmp = []
                for k in pixels[i, j]:
                    keypart = key.pop(0)
                    x = self._backward_l(keypart[0], keypart[1], keypart[2], keypart[3])
                    x = (x * (255+self.offset_range[1]-self.offset_range[0])) - keypart[4]
                    tmp.append(int(x))
                pixels[i, j] = tuple(tmp)

        return image
    
    