from PIL import Image


class ImageEncryptDecrypter:
    def __init__(self, name: str='Image Encrypt/Decrypt', image_mode='rgb', **kwargs):
        self.name = name
        self.image_mode = image_mode
        self._key_history = {}
        if self.image_mode == 'rgb':
            self.pixel_size = 3
        else:
            self.setup_encrypter(kwargs=kwargs)
    
    def __repr__(self) -> str:
        return f'{self.name} (used {len(self._key_history)} times)'
    
    def setup_encrypter(**kwargs):
        pass

    def key_history(self) -> dict:
        return self._key_history
    
    def encrypt(self, image: Image, name=None) -> tuple:
        im, key = self.encrypt_action(image=image)
        self._key_history[name if name else image.filename] = key
        return im, key
    
    def encrypt_action(self, image: Image, key=None):
        pass

    def decrypt(self, key, image: Image) -> Image:
        pass

    def keygen(self, image: Image):
        pass
    
    