from PIL import Image
from .SimpleStream import SimpleStream
import numpy as np


class HenonMapStream(SimpleStream):
    def __init__(self, name: str='HenonMapEncrypter', x: float=0.1):
        super().__init__(name)
        self.x = x
    
    @staticmethod
    def henon_1d_map(x: float, n: int, xprev: float, a: float=1.4, b:float=0.3) -> float:
        return x if n==0 else HenonMapStream.henon_1d_map(b*xprev + 1 - a*x*x, a, b, n-1, x)
    
    @staticmethod
    def henon_1d_map_all_values(x: float, xprev: float, num_values: int, a: float=1.4, b: float=0.3, offset=100000):
        result = []
        for _ in range(offset):
            tmp = x
            x = b*xprev + 1 - a*x*x
            xprev = tmp

        curr_bits = []
        
        for i in range((num_values*8)+1):
            tmp = x
            x = b*xprev + 1 - a*x*x
            xprev = tmp

            curr_bits.append('0' if x <= 0.365 else '1')

            if i!=0 and i%8==0:
                result.append(int(''.join(curr_bits), 2))
                curr_bits = []
        return result
    
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
    
    def keygen(self, image: Image, size: tuple):
        values = np.array(
            HenonMapStream.henon_1d_map_all_values(
                x=self.x,
                xprev=0.5,
                num_values=size[0]*size[1]*self.pixel_size
            )
        )
        
        values = (255*(values - np.min(values))/np.ptp(values)).astype(int)
        return np.reshape(
            values,
            newshape=(size[0], size[1], self.pixel_size)
        )
