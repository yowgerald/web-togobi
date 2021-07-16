import React, { Component } from 'react';
import axios from 'axios';
import { config, fileType } from '../Constants';

const API_URL = config.url.API_URL;

export class ContentFile extends Component {
    constructor(props) {
        super(props);
        this.state = {
            files: [],
            next_page: null,
            prev_page: null,
        };
    }

    handleLoadNext() {
        this.getContentFiles(this.state.next_page);
    }

    handleLoadPrevious() {
        this.getContentFiles(this.state.prev_page);
    }

    async getContentFiles(page = 1) {
        var content = this.props.content;
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
        this.getContentFiles();
    }

    render() {
        var file_count = this.state.files.length;
        var galleryClass = file_count > 1 ? 'gallery' : '';
        var files = this.state.files.map((file, i) => {
            // TODO: may need to use external player for video
            // TODO: when item is clicked, should be fullscreen
            var class_suffix = i + 1;
            if (file_count < 5) {
                if (file_count % 2 === 0 && (file_count === class_suffix)) {
                    class_suffix += ' item__stretch';
                } else if (file_count === 3 && (class_suffix === 2 || class_suffix === 3)) {
                    class_suffix += ' item__stretch--'+class_suffix;
                }
            }
            return [
                <figure key={"gallery__item"+file.id} className={"gallery__item gallery__item--" + class_suffix}>
                    {(() => {
                        if (file.f_type === fileType.IMAGE){
                            return (
                              <img key={"src" + file.id} className="gallery__media" src={file.signed_url} alt=""/>
                            );
                        } else if(file.f_type === fileType.VIDEO) {
                            return (
                                <video key={"src" + file.id} className="gallery__media" src={file.signed_url} alt="" controls/>
                            );
                        }
                        return null;
                    })()}
                </figure>
            ];
        });
        
        return [
            <section key="gallery" className={galleryClass}>
                {files}
            </section>,
            <br key="gallery-load-break"/>,
            <div key="items-page" className="items__page">
                {this.state.prev_page != null ?
                    <div key="load-previous" onClick={() => this.handleLoadPrevious()}>
                        Previous
                    </div>
                : null}
                {this.state.prev_page != null && this.state.next_page ? <span>&nbsp; &bull; &nbsp;</span> : null}
                {this.state.next_page != null ?
                    <div key="load-next" onClick={() => this.handleLoadNext()}>
                        Next
                    </div>
                : null}
            </div>
        ]
    }
}