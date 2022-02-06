import React, { useEffect, useState, useCallback } from "react";
import { BasicInputs } from "./fields/BasicInputs";
import axios from 'axios';
import { config, csrftoken, getFileType, uploadStatus } from '../../Constants';
import { initContentDetails } from "../../Initializers";
import uuid from 'react-uuid';

export const Edit = ({ content, }) => {

    const [contentDetails, setContentDetails] = useState(initContentDetails);
    const [files, setFiles]                   = useState([]);
    const [isRan, setIsRan]                   = useState(false);


    const contentDetailsAPI                   = config.API_URL + '/content/' + content;
    const contentFileUploadAPI                = config.API_URL + '/contents/' + content + '/content_file/upload';
    const contentFilesAPI                     = config.API_URL + '/contents/' + content + '/content_files';

    const getContentDetails = useCallback(
        () => {
            axios.get(contentDetailsAPI, {
                headers: {
                    'X-CSRFToken': csrftoken
                },
            }).then(response => {
                setContentDetails(response.data.result)
            }).catch(error => {
                console.log(error);
            });
    }, [contentDetailsAPI])

    const uploadFile =  useCallback(
        () => {
        let que_files = files.filter(f => f.upload_status === uploadStatus.IN_QUEUE);
    
        for (let qfile of que_files) {
            let formData = new FormData();
            formData.append('file', qfile.blob);

            axios.post(contentFileUploadAPI,
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'X-CSRFToken': csrftoken
                    }
                }
                ).then(response => {
                    let updateFiles = [ ...files ];

                    updateFiles.forEach(ufile => {
                        if(ufile.id === qfile.id) {
                            ufile.upload_status = uploadStatus.DONE;
            
                            // change file id for deleting purposes
                            ufile.id = response.data.result;
            
                            return false;
                        }
                    });
            
                    setFiles(updateFiles);
                }).catch(error => {
                    console.log(error);
                });
        }
    }, [contentFileUploadAPI, files])

    const getContentFiles = useCallback(
        () => {
        axios.get(contentFilesAPI, {
            params: {}
        }).then(response => {
            let currentFiles = response.data.result;

            currentFiles.forEach(cfile => {
                cfile.upload_status = uploadStatus.DONE;
            });
            
            setFiles(currentFiles);
            setIsRan(true);
        }).catch(error => {
            console.log(error);
        })
    }, [contentFilesAPI]);

    useEffect(() => {
        getContentDetails();
        uploadFile();

        if (! isRan) {
            getContentFiles();
        }
    }, [getContentDetails, uploadFile, getContentFiles, isRan])

    // change the active status
    const handleStatus = e => {
        let c_ds = {...contentDetails}
        c_ds.is_active = !contentDetails.is_active;
        setContentDetails(c_ds);
    }

    const handleChange = e => {
        if (typeof e === 'undefined') {
            return false;
        }

        let fi = e.target;

        if (fi.files.length > 0) {
            for (let i = 0; i < fi.files.length; i++) {
                let blob = fi.files[i];
                let tmpUrl = URL.createObjectURL(blob);

                let nfile = {
                    id: uuid(),
                    name: blob.name,
                    signed_url: tmpUrl,
                    upload_status: uploadStatus.IN_QUEUE,
                    blob: blob,
                    f_type: getFileType(blob)
                };

                setFiles(prevFiles => [...prevFiles, nfile]);
            }
        }
    }

    const listFiles = files.map((file) =>
        <li key={file.id}>
            {file.name.substring(0, 20) + "..."}
            <span className="badge secondary">{file.upload_status}</span>
        </li>
    );

    const basicInputProps = { contentDetails, handleStatus };

    return (
        <React.Fragment>
            <div className="row">
                <div className="columns small-12 large-6">
                    <BasicInputs {...basicInputProps}/>
                </div>
                <div className="columns small-12 large-6">
                    <label key="uploader-label" htmlFor="content-file" className="button">Upload File</label>
                    <input key="uploader" id="content-file" name="content-file" className="show-for-sr" type="file" multiple onChange={(e) => handleChange(e)}/>

                    <ul>{listFiles}</ul>
                </div>
            </div>
        </React.Fragment>

    )
}