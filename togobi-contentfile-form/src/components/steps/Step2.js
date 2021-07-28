import React, { Component } from 'react';
import axios from 'axios';
import { config, uploadStatus } from '../../Constants';
import uuid from 'react-uuid';

const API_URL = config.url.API_URL;
const EL_CSRF =  document.querySelector("input[name='csrfmiddlewaretoken'")
const csrftoken = EL_CSRF !== null ? EL_CSRF.value : null;

export class Step2 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            files: [],
            next_page: null,
            prev_page: null,
            fileClasses: [
                null,
                'gallery__item--1',
                'gallery__item--2',
                'gallery__item--3',
                'gallery__item--4',
                'gallery__item--5'
            ],
        };
    }

    handleChange(e) {
        if (typeof e !== 'undefined') {
            var fi = e.target;
            var files = [];
            if(fi.files.length > 0) {
                for (var i = 0; i < fi.files.length; i++) {
                    var blob = fi.files[i];
                    var tmpUrl = URL.createObjectURL(blob);
                    var nfile = {
                        id: uuid(),
                        signed_url: tmpUrl,
                        upload_status: uploadStatus.IN_QUEUE,
                        blob: blob
                    };
                    files.push(nfile)
                }

                this.setState((prevState) => ({
                    files: prevState.files.concat(files)
                }), () => {
                    let que_files = this.state.files.filter(f => f.upload_status === uploadStatus.IN_QUEUE);
                    for (let file of que_files) {
                        this.uploadContentFile(file);
                    }
                });
            }
        }
    }

    handleRemove(id) {
        // TODO: remove from backend/ cloud storage
        this.setState({
            files: this.state.files.filter(f => f.id !== id)
        });
    }

    updateFileUploadStatus(id, status) {
        this.setState((prevState) => {
            let files = [ ...prevState.files ];
            for (let file of files) {
                if(file.id === id) {
                    file.upload_status = status;
                    break;
                }
            }
            
            return { files };
        });
    }

    async uploadContentFile(file) {
        var formData = new FormData();
        formData.append('file', file.blob);
        // TODO: in queue indicator problem
        this.updateFileUploadStatus(file.id, uploadStatus.IN_PROGRESS);
        await axios.post(API_URL+ '/contents/' + this.props.content + '/content_file/upload',
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': csrftoken
                }
            }
            ).then(response => {
                this.updateFileUploadStatus(file.id, uploadStatus.DONE)
            }).catch(error => {
                console.log(error);
                // TODO: may need to return something.
            });
    }

    async getContentFiles(content, page = 1) {
        await axios.get(API_URL + '/contents/' + content + '/content_files', {
                params: {
                    page: page
                }
            }).then(response => {
                this.setState({
                    files: response.data.result,
                    next_page: response.data.next,
                    prev_page: response.data.previous
                });
            }).catch(error => {
                console.log(error);
                // TODO: may need to return something.
            });
    }

    componentDidMount() {
        this.getContentFiles(this.props.content);
    }

    render() {
        if (this.props.currentStep !== 2) {
            return null
        }
        return (
            <React.Fragment>
                <label key="uploader-label" htmlFor="content-file" className="button">Upload File</label>
                <input key="uploader" id="content-file" name="content-file" className="show-for-sr" type="file" multiple onChange={(e) => this.handleChange(e)}/>
                <section key="uploader-gallery" className="gallery">
                    {this.state.files.map((file, i) => (
                        <div key={"item" + file.id} className={this.state.fileClasses[(i + 1)]}>
                            <div className="uploading-indicator">{file.upload_status}</div>
                            {(() => {
                                if (file.blob.type.match('image.*')) {
                                    return (
                                        <img className="gallery__media" src={file.signed_url} alt=""/>
                                    );
                                } else if (file.blob.type.match('video.*')) {
                                    return (
                                        <video className="gallery__media" src={file.signed_url} alt="" controls/>
                                    );
                                }
                            })()}
                            <button className="hollow button tiny alert file-remove" onClick={(e) => this.handleRemove(file.id, e)}>&#x2716;</button>
                        </div>
                    ))}
                </section>
            </React.Fragment>
        )
    }
}