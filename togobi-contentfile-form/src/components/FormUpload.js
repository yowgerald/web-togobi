import React, { Component } from 'react';
import axios from 'axios';
import { config } from '../Constants';

const API_URL = config.url.API_URL;

export class FormUpload extends Component {
    constructor() {
        super();
        this.state = {
            files: [],
            next_page: null,
            prev_page: null
        };
    }

    handleChange(e) {
        if (typeof e !== 'undefined') {
            var fi = e.target;
            var files = [];
            if(fi.files.length > 0) {
                for (var i = 0; i < fi.files.length; i++) {
                    var tmpUrl = URL.createObjectURL(e.target.files[i]);
                    var nfile = {
                        id: i,
                        name: fi.files.item(i).name,
                        tmp_url: tmpUrl,
                    }
                    files.push(nfile)
                }
                this.setState({
                    files: files
                });
            }

            // TODO: manage files layout
            var file_count = this.state.files.length;
            if (file_count < 5) {
                switch (file_count) {
                    case 1:
                        // TODO: adjust grid system
                        break;
                }
            }
            console.log(this.state.fileClass)
        }
    }

    handleRemove(id) {
        this.setState({
            files: this.state.files.filter(f => f.id !== id)
        });
        var excluded = document.querySelector('#exclusions');
        var exs = excluded.value || '';
        excluded.value = exs + '' + (exs !== '' ? ','+id : id)
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
            <label htmlFor="content-file" className="button" key="uploader-label">Upload File</label>,
            <input id="content-file" name="content-file" className="show-for-sr" type="file" multiple key="uploader" onClick={(e) => this.handleChange(e)}/>,
            <input id="exclusions" name="exclusions" hidden key="excluded"/>,
            <ul key="file-list">
              {this.state.files.map((file) => (
                <li key={file.id}>
                  <img src={file.tmp_url} alt=""/>
                  <button className="hollow button tiny alert" onClick={this.handleRemove.bind(this, file.id)}>remove</button>
                </li>
              ))}
            </ul>
          ]
    }
}