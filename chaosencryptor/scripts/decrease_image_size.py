from typing_extensions import ParamSpec
from PIL import Image
import argparse

def save_image(image, path=None):
    out = path if path else f'{image.filename}_resized.png'
    image.save(out)

def downsize(image, size):
    image.thumbnail(size, Image.ANTIALIAS)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='The input image path')
    parser.add_argument('-o', required=False, help='The output image path')
    parser.add_argument('-x', required=False, default=100, type=int)
    parser.add_argument('-y', required=False, default=100, type=int)

    args = parser.parse_args()
    image = Image.open(args.i)
    downsize(image, (args.x, args.y))
    save_image(image, args.o)

if __name__ == '__main__':
    main()