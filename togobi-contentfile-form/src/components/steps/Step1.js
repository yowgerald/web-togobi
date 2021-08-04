import React, { Component } from 'react';
import axios from 'axios';
import { config, csrftoken, formMode } from '../../Constants';

export class Step1 extends Component {
    constructor (props) {
        super(props);
        this.state = {
            content_details: {
                title: '',
                description: '',
                tags: '',
                target_date: null,
                is_active: false,
            },
        };
    }

    async getContentDetails(id) {
        await axios.get(config.url.API_URL + '/content/' + id, {
                headers: {
                    'X-CSRFToken': csrftoken
                },
            }).then(response => {
                this.setState({
                    content_details: response.data.result
                })
            }).catch(error => {
                console.log(error);
                // TODO: may need to return something.
            });
    }

    handleStatus() {
        var content_details = {...this.state.content_details}
        content_details.is_active = !content_details.is_active;
        this.setState({content_details})
    }

    componentDidMount() {
        if (this.props.mode === formMode.EDIT) {
            this.getContentDetails(this.props.content);
        }
    }

    render() {
        return (
            <React.Fragment>
                <p>
                    <label htmlFor="id_title">Title:</label>
                    <input type="text" name="title" defaultValue={this.state.content_details.title} maxLength="200" required="" id="id_title"></input>
                </p>
                <p>
                    <label htmlFor="id_description">Description:</label>
                    <textarea name="description" defaultValue={this.state.content_details.description} cols="20" rows="5" maxLength="200" required="" id="id_description"></textarea>
                </p>
                <p>
                    <label htmlFor="id_tags">Tags:</label>
                    <input type="text" name="tags" defaultValue={this.state.content_details.tags} maxLength="200" required="" id="id_tags"></input>
                </p>
                <p>
                    <label htmlFor="id_target_date">Target date:</label>
                    <input type="datetime-local" name="target_date" defaultValue={this.state.content_details.target_date} required="" id="id_target_date"></input>
                </p>
                <p>
                    <label htmlFor="id_is_active">Active:</label>
                    <input type="checkbox" name="is_active" id="id_is_active" checked={this.state.content_details.is_active} onChange={() => this.handleStatus()}></input>
                </p>
            </React.Fragment>
        )
    }
}