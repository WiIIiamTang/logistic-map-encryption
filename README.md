# Image encryption with the chaotic logistic map

Image encryption with XOR cipher, XOR cipher with Logistic Map, XOR cipher with Henon Map, and Logistic Map Pixel Iterations.


## Info
View the [webapp](https://logistic-map-326.herokuapp.com/) to try it out. 

**For more information on encryption tools and a standalone package for image encryption, go to ``chaosencryptor``, or [click this link](https://github.com/WiIIiamTang/logistic-map-encryption/tree/main/chaosencryptor).**

## Dev

To run the website,
```sh
npm install
npm run start
```

To run the server,
```sh
pip3 install pipenv
pipenv install
pipenv shell
python app.py
```

You can run both instances at the same time, but you need to set the ``api_base`` URL in ``EncryptDecryptMenu`` to the Flask server.

### Production
```sh
npm run dbuild
```
To build into the ``templates``. The site is served as a Flask app. 

The sample images need to be moved into wherever your static directory is (by default ``templates/static``).

##  Acknowledgements

One method used in this project was partly based on the works of Ahmad et al.

I. Ahmad, A. Soleymani, M. J. Nordin, and E. Sundararajan, "A chaotic cryptosystem for images based on henon and arnold cat map," pp. 2356–6140, 08 2014

This project was done for a course on Nonlinear Dynamics and Chaos at McGill University. View the license for this repo [here](https://github.com/WiIIiamTang/logistic-map-encryption/blob/main/LICENSE.txt).
