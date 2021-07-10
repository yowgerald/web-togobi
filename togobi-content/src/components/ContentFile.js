import React, { Component } from 'react';
import axios from 'axios';
import { config } from '../Constants';

const API_URL = config.url.API_URL;

export class ContentFile extends Component {
    constructor(props) {
        super(props);
        this.state = {
            files: [],
            next_page: null,
            prev_page: null,
        };

        this.handleLoadMore = this.handleLoadMore.bind(this);
    }

    handleLoadMore() {
        this.getContentFiles(this.state.next_page);
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
        var files = this.state.files.map((file, i) => {
            var isFirstItem = i === 0 ? true : false;
            var inputElement = <input type="radio" id={file.id} name="gallery" className="gallery__selector"/>;
            if (isFirstItem) {
                inputElement = <input type="radio" id={file.id} name="gallery" className="gallery__selector" defaultChecked/>;
            }
            return [
                <div key={"gallery__item"+file.id} className="gallery__item">
                    {inputElement}
                    {/* TODO: adjust the preview size if less than 3 */}
                    <img className="gallery__img" src={file.signed_url} alt=""/>
                    <label htmlFor={file.id} className="gallery__thumb">
                        <img src={file.signed_url} alt=""/>
                    </label>
                </div>
            ];
        });
        
        return (
            // TODO: what happens to uploaded videos?
            // TODO: add previous?
            <section className="gallery">
                {files}
                {this.state.next_page != null ?
                    <div className="gallery__item">
                        <div className="gallery__thumb" onClick={() => this.handleLoadMore()}>
                            <h4>Load More</h4>
                        </div>
                    </div>
                : null}
                
            </section>
        )
    }
}