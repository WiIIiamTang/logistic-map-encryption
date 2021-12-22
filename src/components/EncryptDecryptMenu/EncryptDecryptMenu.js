import EncryptDecryptOptions from "../EncryptDecryptOptions/EncryptDecryptOptions";
import ImageForm from "../ImageForm/ImageForm";
import OutputMenu from "../OutputMenu/OutputMenu";
import useStyles from './styles';
import { useState } from 'react';

const EncryptDecryptMenu = () => {
    const classes = useStyles();
    const [outImg, setOutImg] = useState(null);
    const [generatedKey, setGeneratedKey] = useState(null);
    const [uploadedKey, setUploadedKey] = useState('');
    const [model, setModel] = useState('SimpleStream');
    const [waiting, setWaiting] = useState(false);

    const api_base = '';

    return (
        <div className={classes.mainMenu}>
            <ImageForm api_base={api_base}/>
            
            <EncryptDecryptOptions setWaiting={setWaiting} setModel={setModel} model={model} api_base={api_base} uploadedKey={uploadedKey} setOutImg={setOutImg} setGeneratedKey={setGeneratedKey} setUploadedKey={setUploadedKey}/>
            
            <OutputMenu waiting={waiting} model={model} api_base={api_base} outImg={outImg} generatedKey={generatedKey}/>
        </div>
    )
}

export default EncryptDecryptMenu
