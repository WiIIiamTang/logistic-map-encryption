import { useState, useEffect } from "react";
import { Button, CircularProgress, TextField } from "@material-ui/core";
import { DropzoneDialog } from "material-ui-dropzone";
import axios from "axios";
import useStyles from "./styles";

const OutputMenu = ({ waiting, api_base, outImg, generatedKey }) => {
    const classes = useStyles();
    const [show, setShow] = useState(false);
    const [imageFile, setImageFile] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const [progress, setProgress] = useState(null);
    const [imageId, setImageId] = useState(0);
    const [currentlyUploading, setCurrentlyUploading] = useState(false);
    


    const get_image_url = (id) => {
        console.log("GET IMAGE URL");
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
                });
    };

    const handleFile = ([file]) => file && setImageFile(file);
    const handleDelete = () => setImageFile(null);
    const handleSubmit = ([file]) => {
        const fd = new FormData();
        fd.append("file", file, file.name);
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

    // const downloadKey = () => {
    //     window.location.href = `${api_base}${generatedKey}`;
    // };

    return (
        <div className={classes.muiVersion}>
            <h2>Output</h2>
            <div className={classes.imageSection}>
                {waiting && 
                    <>
                        <CircularProgress/>
                    </>}
                {outImg ? (
                    <>
                        <img
                            className={classes.img}
                            src={`${api_base}${outImg}`}
                            alt="material ui version preview"
                        />
                        <a
                            className={classes.link}
                            href={`${api_base}${outImg}`}
                            target="_blank"
                            rel="noreferrer"
                        >
                            link
                        </a>
                    </>
                ) : (
                    <p className={classes.nopic}>no image generated</p>
                )}


            </div>
            <div>
                {generatedKey ? (
                    
                    <div style={{height: '100px', overflow: 'auto', width: '200px', backgroundColor: 'red'}}>
                    {generatedKey}
                    </div>
                ): 'no key'}
            </div>
            {/* <Button variant="contained" onClick={downloadKey}>
                Download generated key
            </Button> */}
        </div>
    );
};

export default OutputMenu;
