import models
import argparse
import json
from PIL import Image

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required='True', help='Path to input PNG image')
    parser.add_argument('-o', required='True', default='outputs/decrypted.png', help='Path to output decrypted PNG image')
    parser.add_argument('-m', required=True, default='SimpleStream', help='The decryption model')
    parser.add_argument('--keypath', required='True', default='key.key', help='Path to generated key')

    return parser.parse_args()

def decrypt(decrypter, image_path, key):
    return decrypter.decrypt(key=key, image=Image.open(image_path).convert('RGB'))

def save_results(image, o):
    image.save(o)

def main():
    args = setup_args()
    decrypter = getattr(models, args.m)()

    with open(args.keypath, 'rb') as f:
        key = json.load(f)
    
    image = decrypt(decrypter, args.i, key)
    save_results(image, args.o)

if __name__ == '__main__':
    main()

