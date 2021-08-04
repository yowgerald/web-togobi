import React, { Component } from 'react';
import axios from 'axios';
import { config } from '../../Constants';

const API_URL = config.url.API_URL;
const EL_CSRF =  document.querySelector("input[name='csrfmiddlewaretoken'")
const csrftoken = EL_CSRF !== null ? EL_CSRF.value : null;

export class Step1 extends Component {
    constructor (props) {
        super(props);
        this.state = {
            html: '',
            content_details: {
                title: '',
                description: '',
                tags: '',
                target_date: null,
                is_active: false,
            },
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

    async getContentDetails(id) {
        await axios.get(API_URL + '/content/' + id, {
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

    componentDidMount() {
        // this.getFormContent(this.props.content);
        this.getContentDetails(this.props.content);
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
                    <input type="checkbox" name="is_active" id="id_is_active" checked={this.state.content_details.is_active} onChange={() => {}}></input>
                </p>
            </React.Fragment>
        )
    }
}