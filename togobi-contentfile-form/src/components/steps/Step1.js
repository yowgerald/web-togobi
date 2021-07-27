import React, { Component } from 'react';
import axios from 'axios';
import { config } from '../../Constants';

const API_URL = config.url.API_URL;

export class Step1 extends Component {
    constructor (props) {
        super(props);
        this.state = {
            html: '',
        };
    }

    async getFormContent(id = null) {
        // get Html Form from backend
        await axios.get(API_URL + '/form/content', {
                params: {
                    id: id
                }
            }).then(response => {
                this.setState({
                    html: response.data.form
                })
            }).catch(error => {
                console.log(error);
                // TODO: may need to return something.
            });
    }

    componentDidMount() {
        let content = isNaN(this.props.content) ? null : this.props.content;
        this.getFormContent(content);
    }

    render() {
        if (this.props.currentStep !== 1) {
            return null
        }
        return (
            <div dangerouslySetInnerHTML={{ __html: this.state.html }} />
        )
    }
}