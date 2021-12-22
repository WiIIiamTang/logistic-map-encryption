from typing_extensions import ParamSpec
from PIL import Image
import argparse

def save_as_png(image, path=None):
    out = path if path else f'{image.filename}_converted.png'
    image.save(out, format='png')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='The input image path')
    parser.add_argument('-o', required=False, help='The output image path')
    args = parser.parse_args()
    image = Image.open(args.i)
    save_as_png(image, args.o)

if __name__ == '__main__':
    main()