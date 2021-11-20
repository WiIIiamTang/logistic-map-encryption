import { useState, useEffect } from 'react';
import { Button } from '@material-ui/core';
import { DropzoneDialog } from 'material-ui-dropzone';
import axios from 'axios';
import useStyles from './styles';

const ImageForm = () => {
    const api_base = ''
    const classes = useStyles();
    const [show, setShow] = useState(false);
    const [imageFile, setImageFile] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const [progress, setProgress] = useState(null);
    const [imageId, setImageId] = useState(null);
    const [currentlyUploading, setCurrentlyUploading] = useState(false);

    const get_image_url = (id) => {
        console.log('GET IMAGE URL');
        id &&
        axios
        .get(`${api_base}/images/${id}`)
        .then((response) => {
            console.log(response);
            const data = response.data;
            setImageUrl(data.url);
        })
        .catch((err) => {
            console.log(err);
        })
    }

    const handleFile = ([file]) => file && setImageFile(file);
    const handleDelete = () => setImageFile(null);
    const handleSubmit = ([file]) => {
        const fd = new FormData();
        fd.append('file', file, file.name);
        axios
        .post(`${api_base}upimg`, fd)
        .then((response) => {
            console.log(response);
            const data = response.data;
            setImageId(data.id);
            setImageUrl(data.url);
            setImageFile(null);
            setCurrentlyUploading(false);
            setShow(false);
        })
        .catch((err) => {
            console.log(err);
            alert(err);
            setCurrentlyUploading(false);
            setShow(false);
        });
    };

    // useEffect(() => {
    //     get_image_url(imageId);
    // }, [imageId])

    return (
        <div className={classes.muiVersion}>
        <div className={classes.imageSection}>
            {imageId ? (
            <>
                <img
                className={classes.img}
                src={`${api_base}${imageUrl}`}
                alt='material ui version preview'
                />
                <a
                className={classes.link}
                href={`${api_base}${imageUrl}`}
                target='_blank' rel="noreferrer"
                >
                link
                </a>
            </>
            ) : (
            <p className={classes.nopic}>no mui version pic yet</p>
            )}
        </div>
        <Button className={classes.btn} onClick={() => setShow(true)}>
            mui version
        </Button>
        <DropzoneDialog
            open={show}
            onChange={handleFile}
            onClose={() => setShow(false)}
            onDelete={handleDelete}
            acceptedFiles={['image/png']}
            maxFileSize={5000000}
            filesLimit={1}
            showFileNamesInPreview={false}
            showFileNames={false}
            dropzoneText={'Drop it here'}
            getFileAddedMessage={() => 'file added!'}
            getFileRemovedMessage={() => 'file removed!'}
            onAlert={(alert) => console.log({ alert })}
            getFileLimitExceedMessage={() => 'file is too big'}
            getDropRejectMessage={(file) => {
            if (file.size > 5000000) return 'file is too big';
            else return 'invalid file type';
            }}
            onSave={handleSubmit}
        />
        </div>
    );
};

export default ImageForm;
