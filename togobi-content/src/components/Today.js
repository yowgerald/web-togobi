import React, { Component } from 'react';
import axios from 'axios';
import { config } from '../Constants';

const API_URL = config.url.API_URL;

export class Today extends Component {
    constructor() {
        super();
        this.state = {
            contents_today: []
        };
    }

    async getContentsToday(query = null) {
        await axios.get(API_URL+'/contents/today',
            {
                params: {
                    q: query
                }
            }).then(response => {
                this.setState({ contents_today: response.data })
            })
            .catch(error => {
                console.log(error);
            });
    }

    componentDidMount() {
        this.getContentsToday();
    }

    render() {
        return (
            <div className="row column">
                <p className="lead">TODAY</p>
                {this.state.contents_today.length > 0 ? 
                    this.state.contents_today.map((content) => {
                        return (
                            <p key={"title"+content.id}>{content.title}</p>
                        )
                    })
                :
                    <p>No items available yet.</p>
                }
                
            </div>
        )
    }
}