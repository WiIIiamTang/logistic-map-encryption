import models
import argparse
import pickle
from PIL import Image

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required='True', help='Path to input PNG image')
    parser.add_argument('-o', required='True', default='outputs/encrypted.png', help='Path to output encrypted PNG image')
    parser.add_argument('-m', required=True, default='SimpleStream', help='The encryption model')
    parser.add_argument('--keypath', required='True', default='key.key', help='Path to generated key')

    return parser.parse_args()

def encrypt(encrypter, image_path, name=None):
    im = Image.open(image_path)
    name = im.filename
    return encrypter.encrypt(image=im.convert('RGB'), name=name)

def save_results(image, key, o, keypath):
    image.save(o)
    with open(keypath, 'wb') as f:
        pickle.dump(key, f)

def main():
    args = setup_args()
    encrypter = getattr(models, args.m)()
    image, key = encrypt(encrypter, args.i)
    save_results(image, key, args.o, args.keypath)

if __name__ == '__main__':
    main()

