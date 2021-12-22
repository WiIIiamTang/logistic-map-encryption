# Image encryption and decryption library

This contains the code needed to encrypt or decrypt images with certain models. It can be used as a standalone package, or be used with the webapp.

**This directory also contains results and outputs used in the final report of this project.** See the ``outputs`` directory for a full list of images.

## Models

Current models:

- Simple XOR cipher
- XOR cipher with Logistic Map
- XOR with Henon map
- Logistic map pixel iterator

### Implementing a compatible encryption model

Models are built off a base class ``ImageEncryptDecrypter`` that provides an easy way to extend or create new compatible models.
**You do not need to override the ``encrypt`` function**. To create a model, you only need to

- Implement ``keygen`` which generates a key for the encryption/decryption process.

- **If ``keygen`` relies on parameter settings**, you may need to implement some other function to generate the "real" key to be used during decryption. For example, when using the logistic map XOR method, the key generated is simply some initial conditions for the logistic map. So we had to create ``create_keymap`` to generate the actual matrix to XOR the image with.

- Finally, implement the ``encrypt_action`` and ``decrypt`` functions.


## Encryption/Decryption

Use ``encrypt.py`` or ``decrypt.py``:

```
usage: encrypt.py [-h] -i I -o O -m M --keypath KEYPATH

optional arguments:
  -h, --help         show this help message and exit
  -i I               Path to input PNG image
  -o O               Path to output encrypted PNG image
  -m M               The encryption model
  --keypath KEYPATH  Path to generated key
 ```
 
 ```
 usage: decrypt.py [-h] -i I -o O -m M --keypath KEYPATH

optional arguments:
  -h, --help         show this help message and exit   
  -i I               Path to input PNG image
  -o O               Path to output decrypted PNG image
  -m M               The decryption model
  --keypath KEYPATH  Path to generated key
 ```
 
 ## Utility scripts
 
 In ``scripts``:
 
 - ``decrease_image_size.py``: Scales down the image dimensions.
 - ``plot_image_histogram.py``: Plots the image histogram for a given image. The distribution is shown for red, green and blue.
 - ``save_as_png.py``: Converts an image to PNG. This shouldn't be used anymore. Instead, save it as a PNG directly in Pillow.
