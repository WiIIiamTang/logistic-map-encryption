import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import argparse
from PIL import Image

def as_hex(red=0, green=0, blue=0):
    return f'#{red:02X}{green:02X}{blue:02X}'

def plot_and_save(image, name=None):
    hist_data = image.histogram()
    hist_data = [hist_data[i:i+256] for i in range(0, len(hist_data), 256)]
    gs = gridspec.GridSpec(6, 1)
    f = plt.figure()

    redplt = f.add_subplot(gs[0:2, 0])
    redplt.set_title(label='Distribution of Red')
    for i in range(256):
        redplt.bar(i, hist_data[0][i], color = as_hex(red=i), edgecolor=as_hex(red=i), alpha=0.4)

    greenplt = f.add_subplot(gs[2:4, 0])
    greenplt.set_title(label='Distribution of Green')
    for i in range(256):
        greenplt.bar(i, hist_data[0][i], color = as_hex(green=i), edgecolor=as_hex(green=i), alpha=0.4)
        
    blueplt = f.add_subplot(gs[4:6, 0])
    blueplt.set_title(label='Distribution of Blue')
    for i in range(256):
        blueplt.bar(i, hist_data[0][i], color = as_hex(blue=i), edgecolor=as_hex(blue=i), alpha=0.4)

    gs.update(wspace=1, hspace=10.5)
    f.savefig(name if name else f'{image.filename}_histograms.png')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='The input image path')
    parser.add_argument('-o', required=False, help='The output image path')

    args = parser.parse_args()
    image = Image.open(args.i)
    plot_and_save(image, args.o)

if __name__ == '__main__':
    main()