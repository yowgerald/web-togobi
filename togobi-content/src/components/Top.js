import React, { Component } from 'react';
import axios from 'axios';
import { config } from '../Constants';

export class Top extends Component {
    
    constructor() {
        super();
        this.state = {
            contents_top: [],
        }
    }

    async getContentsTop(query = null) {
        await axios.get(config.API_URL + '/contents/top',
            {
                params: {
                    q: query
                }
            }).then(response => {
                this.setState({ contents_top: response.data })
            })
            .catch(error => {
                console.log(error);
            });
    }

    componentDidMount() {
        this.getContentsTop();
    }
    
    render() {
        return (
            <div className="row column">
                <p className="lead">TOP</p>
                {this.state.contents_top.length > 0 ? 
                    this.state.contents_top.map((content) => {
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