import EncryptDecryptMenu from './components/EncryptDecryptMenu/EncryptDecryptMenu';

const App = () => {
  return (
    <div>
      <h1>Image Encryption with chaotic maps</h1>
      <p>This tool demonstrates various methods of image encryption using a discrete chaotic map.
      For more information, consult the <a href="https://github.com/WiIIiamTang/logistic-map-encryption" target="_blank" rel="noreferrer">
      Github repository</a> for this project.</p>

      <h2>Encryption details</h2>
      <p>You must upload a PNG image in the Input section. Please do not upload anything too large. The preferred size would be 100x100, such as the examples below </p>
      <img src={"/static/lightDino.png"} alt="dino"/>
      <img src={"/static/penguin.png"} alt="dino"/>

      <p>To decrypt, uploaded the encrypted file into Input. Then paste the key into the correct place and press decrypt.</p>

      <h2>SimpleStream</h2>
      <p>An XOR cipher, where the key is a randomly generated sequence of integers between 0 and 255 from a uniform distribution.</p>
      

      <h2>LogisticMapStream</h2>
      <p>An XOR cipher, where the key is a randomly generated sequence of integers between 0 and 255 from the logistic map.</p>

      <h2>HenonMapStream</h2>
      <p>A method involving three XOR ciphers. Keys are created by generating integers between 0 and 255 from the Hénon Map.</p>

      <h2>LogisticMapPixel</h2>
      <p>A method that iterates each pixel of the image with the logistic map. The initial condition of the logistic map is the pixel's value (a number between 0 and 1).</p>
      <p style={{color: 'red'}}>
        Warning: the number of iterations has been set to 10-15 for this app and you <strong>cannot set a key or decrypt</strong> when using this method because of performance reasons. It may take a few minutes to encrypt.
      </p>

      <EncryptDecryptMenu/>


      <p style={{fontSize: '0.85rem', textAlign: 'center', color: "gray"}}>
        MATH 326 - McGill University
      </p>
    </div>
  );
};

export default App;
