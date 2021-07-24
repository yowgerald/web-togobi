import React, { Component } from 'react';
import axios from 'axios';
import { config } from '../Constants';
import uuid from 'react-uuid';


const API_URL = config.url.API_URL;

export class FormUpload extends Component {
    constructor() {
        super();
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
                // TODO: when edit mode don't remove existing file state
                // TODO: need to readjust the index id
                for (var i = 0; i < fi.files.length; i++) {
                    var tmpUrl = URL.createObjectURL(e.target.files[i]);
                    var nfile = fi.files[i];
                    nfile.id = uuid();
                    nfile.signed_url = tmpUrl;
                    files.push(nfile)
                }

                // TODO: save file to backend
                this.setState((prevState) => ({
                    files: prevState.files.concat(files)
                }),() => {
                    console.log(this.state.files);
                });
            }
        }
    }

    handleRemove(id) {
        this.setState({
            files: this.state.files.filter(f => f.id !== id)
        });
    }

    async getContentFiles(content, page = 1) {
        await axios.get(API_URL+'/contents/'+content+'/content_files', 
            {
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
        var container = document.getElementById('root');
        if (container.getAttribute('is-edit')) {
            var content = container.getAttribute('content');
            if (content) {
                this.getContentFiles(content);
            }
        }
    }

    render() {
        return [
            <label key="uploader-label" htmlFor="content-file" className="button">Upload File</label>,
            <input key="uploader" id="content-file" name="content-file" className="show-for-sr" type="file" multiple onChange={(e) => this.handleChange(e)}/>,
            <section key="uploader-gallery" className="gallery">
                {this.state.files.map((file, i) => (
                    <div key={"item" + file.id} className={this.state.fileClasses[(i + 1)]}>
                        {(() => {
                            if (file.type.match('image.*')) {
                                return (
                                    <img className="gallery__media" src={file.signed_url} alt=""/>
                                );
                            } else if (file.type.match('video.*')) {
                                return (
                                    <video className="gallery__media" src={file.signed_url} alt="" controls/>
                                );
                            }
                        })()}
                        <button className="hollow button tiny alert file-remove" onClick={(e) => this.handleRemove(file.id, e)}>&#x2716;</button>
                    </div>
                ))}
            </section>
          ]
    }
}