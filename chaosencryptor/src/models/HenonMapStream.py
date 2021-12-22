from PIL import Image
from .SimpleStream import SimpleStream
import numpy as np
import math

class HenonMapStream(SimpleStream):
    def __init__(self, name: str='HenonMapEncrypter', x: float=0.1, gamma_parameter: int=88888, lambda_parameter: int=44444):
        super().__init__(name)
        self.x = x
        self.gamma_parameter = gamma_parameter
        self.lambda_parameter = lambda_parameter
    
    @staticmethod
    def henon_1d_map(x: float, n: int, xprev: float, a: float=1.4, b:float=0.3) -> float:
        return x if n==0 else HenonMapStream.henon_1d_map(b*xprev + 1 - a*x*x, a, b, n-1, x)
    
    @staticmethod
    def henon_1d_map_all_values_reg(x: float, xprev: float, num_values: int, a: float=1.4, b: float=0.3, offset=100000):
        result = []
        for _ in range(offset):
            tmp = x
            x = b*xprev + 1 - a*x*x
            xprev = tmp
        
        for _ in range(num_values):
            tmp = x
            x = b*xprev + 1 - a*x*x
            xprev = tmp
            
            result.append(x)
        return result
    
    @staticmethod
    def henon_2d_map_all_values(x: float, y: float, num_values: int, a: float=1.4, b: float=0.3, offset: int=100):
        result = []
        for _ in range(offset):
            x, y = (y + 1 - a*x*x, b*x)
        
        for _ in range(num_values):
            x, y = (y + 1 - a*x*x, b*x)
            result.append((x,y))
        
        return result
    
    def keygen(self, image: Image, size: tuple):
        return {
            'x': np.random.uniform(0.1, 0.2),
            'y': np.random.uniform(0.1, 0.2),
            'offset': np.random.randint(100, 200),
            # we always keep the same a, b for this experiment.
            'a': 1.4,
            'b': 0.3
        }

    def create_keymap(self, key: dict, size: tuple) -> any:
        henon_values = HenonMapStream.henon_2d_map_all_values(
            x=key.get('x'),
            y=key.get('y'),
            num_values=size[0]*size[1]*self.pixel_size,
            offset=key.get('offset'),
            a=key.get('a'),
            b=key.get('b')
        )

        sec_img_x = np.reshape(
            np.array([
                int(math.floor(abs(h[0]*self.gamma_parameter)) % 256)
                for h in
                henon_values
            ]),
            newshape=(size[0], size[1], self.pixel_size)
        )

        sec_img_y = np.reshape(
            np.array([
                int(math.floor(abs(h[1]*self.lambda_parameter)) % 256)
                for h in
                henon_values
            ]),
            newshape=(size[0], size[1], self.pixel_size)
        )

        return np.bitwise_xor(sec_img_x, sec_img_y)
