import { Button, FormControl, InputLabel, MenuItem, Select, TextField } from "@material-ui/core"
import useStyles from './styles';
import { useState } from 'react';
import axios from "axios";

const EncryptDecryptOptions = ({ setWaiting, setModel, model, api_base, uploadedKey, setOutImg, setGeneratedKey, setUploadedKey }) => {
    const classes = useStyles();
    const [key, setKey] = useState(null);
    const maxTries = 20;

    const handleEncryptTryAgain = (tries) => {
        if (tries===0) {
            alert('Encrypting failed. Try refreshing the page.');
            return;
        }

        setWaiting(true);
        axios
        .get(`${api_base}/encrypt`, {
            params: {
                model: model
            }
        })
        .then((response) => {
            console.log(response);
            const data = response.data;
            setOutImg(data.url);
            if (model !== 'LogisticMapPixel') {
                setGeneratedKey(data.key);
            }
            setWaiting(false);
        })
        .catch((err) => {
            handleEncryptTryAgain(tries-1);
        })
    }

    const handleEncrypt = () => {
        setWaiting(true);
        axios
        .get(`${api_base}/encrypt`, {
            params: {
                model: model
            }
        })
        .then((response) => {
            console.log(response);
            const data = response.data;
            setOutImg(data.url);
            if (model !== 'LogisticMapPixel') {
                setGeneratedKey(data.key);
            }
            setWaiting(false);
        })
        .catch((err) => {
            handleEncryptTryAgain(maxTries);
        })
    };

    const handleDecryptTryAgain = (tries) => {
        if (tries===0) {
            alert('Error Decrypting. Try refreshing');
            return;
        }

        setWaiting(true);
        const fd = new FormData();
        fd.append('model', model);
        fd.append('keystring', uploadedKey);
        axios
        .post(`${api_base}/decrypt`, fd)
        .then((response) => {
            console.log(response);
            const data = response.data;
            setOutImg(data.url);
            setWaiting(false);
            setGeneratedKey('');
        })
        .catch((err) => {
            handleDecryptTryAgain(tries-1)
        });
    }

    const handleDecrypt = () => {
        setWaiting(true);
        const fd = new FormData();
        fd.append('model', model);
        fd.append('keystring', uploadedKey);
        axios
        .post(`${api_base}/decrypt`, fd)
        .then((response) => {
            console.log(response);
            const data = response.data;
            setOutImg(data.url);
            setWaiting(false);
            setGeneratedKey('')
        })
        .catch((err) => {
            handleDecryptTryAgain(maxTries);
        });
    }

    const handleInput = (input) => {
        setUploadedKey(input);
        setKey(input);
    }

    return (
        <div className={classes.options}>
            <FormControl fullWidth>
                <InputLabel id="input-label">Model</InputLabel>
                <Select
                    labelId="input-label"
                    id="input"
                    value={model}
                    onChange={e => { setModel(e.target.value)}}

                >
                    <MenuItem value={'SimpleStream'}>SimpleStream</MenuItem>
                    <MenuItem value={'LogisticMapStream'}>LogisticMapStream</MenuItem>
                    <MenuItem value={'HenonMapStream'}>HenonMapStream</MenuItem>
                    <MenuItem value={'LogisticMapPixel'}>LogisticMapPixel</MenuItem>
                </Select>
            </FormControl>

            <Button
                variant="contained"
                color="secondary"
                size="large"
                onClick={handleEncrypt}
            >Encrypt</Button>

            {
                (model !== 'LogisticMapPixel') &&
            <Button
                variant="contained"
                color="secondary"
                size="large"
                onClick={handleDecrypt}
            >Decrypt</Button>
            }

            { (model !== 'LogisticMapPixel') &&
            <TextField
                fullWidth
                label={'Paste the keystring if decrypting'}
                variant='outlined'
                onChange={(e) => handleInput(e.target.value)}
            />
            }

            {/* {key && (<div>{key}</div>)} */}
        </div>
    )
}

export default EncryptDecryptOptions
