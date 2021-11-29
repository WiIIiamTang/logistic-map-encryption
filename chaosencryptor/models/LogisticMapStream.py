from PIL import Image
from .SimpleStream import SimpleStream
import numpy as np


class LogisticMapStream(SimpleStream):
    def __init__(self, name: str='LogisticMapEncrypter', x: float=0.5, r: float=3.999):
        super().__init__(name)
        self.x = x
        self.r = r
    
    @staticmethod
    def logistic_map(x: float, r: float, n: int) -> float:
        return x if n==0 else LogisticMapStream.logistic_map(r*x*(1-x), r, n-1)
    
    @staticmethod
    def logistic_map_all_values(x: float, r: float, num_values: int, offset=1000):
        result = []
        for _ in range(offset):
            x = r*x*(1-x)
        
        for _ in range(num_values):
            x = r*x*(1-x)
            result.append(x)
        return result
    
    def keygen(self, image: Image, size: tuple):
        return np.reshape(
            np.array([
                int(x*255) for x in
                LogisticMapStream.logistic_map_all_values(
                    self.x,
                    self.r,
                    size[0]*size[1]*self.pixel_size
                )
            ]),
            newshape=(size[0], size[1], self.pixel_size)
        )
