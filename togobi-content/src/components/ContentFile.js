import React, { Component } from 'react';
import axios from 'axios';
import { config } from '../Constants';

const API_URL = config.url.API_URL;

export class ContentFile extends Component {
    constructor(props) {
        super(props);
        this.state = {
            files: [],
        };

        this.handleLoadMore = this.handleLoadMore.bind(this);
    }

    handleLoadMore() {
        console.log('TODO: implement load more');
        // TODO: increment pagination
    }

    componentDidMount() {
        // TODO: default pagination
        var content = this.props.content;
        axios.get(API_URL+'/contents/'+content+'/content_files')
            .then(response => {
                this.setState({ files: response.data})
            })
            .catch(error => {
                console.log(error);
                // TODO: may need to return something.
            });
    }

    render() {
        var loadMore = null;
        if(this.state.files.length > 0) {
            loadMore = <div className="gallery__item">
            <div className="gallery__thumb" onClick={() => this.handleLoadMore()}>
                    <h4>Load More</h4>
                </div>
            </div>
        }
        var files = this.state.files.map((file, i) => {
            var isFirstItem = i === 0 ? true : false;
            var inputElement = <input type="radio" id={file.id} name="gallery" className="gallery__selector"/>;
            if (isFirstItem) {
                inputElement = <input type="radio" id={file.id} name="gallery" className="gallery__selector" defaultChecked/>;
            }
            return [
                <div key={"gallery__item"+file.id} className="gallery__item">
                    {inputElement}
                    <img className="gallery__img" src={file.signed_url} alt=""/>
                    <label htmlFor={file.id} className="gallery__thumb">
                        <img src={file.signed_url} alt=""/>
                    </label>
                </div>
            ];
        });
        
        return (
            // TODO: what happens to uploaded videos?
            <section className="gallery">
                {files}
                {loadMore}
            </section>
        )
    }
}