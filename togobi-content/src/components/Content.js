import React, { Component } from 'react';
import axios from 'axios';
import { ContentFile } from './ContentFile';

export class Content extends Component {
    constructor(props) {
        super(props);
        this.state = {
            contents: []
        };
    }

    componentDidMount() {
        axios.get('http://localhost:8000/contents')
        .then(response => {
            this.setState({ contents: response.data })
            console.log(response.data)
        })
        .catch(error => {
            console.log(error);
        });
    }

    render() {
        return (
            <div>
                {this.state.contents.map(content => (
                    <div className="card" key={content.id}>
                        {/* TODO: put hrefs value */}
                        <ContentFile files={content.content_files}/>
                        <div className="card-section">
                            <h4><a href="#">{content.title}</a></h4>
                            <p>
                            <span>{ content.description }</span>
                            <br/>
                            <span><i className="fi-calendar">{ content.target_date } &nbsp;&nbsp;</i></span>
                            <br/>
                            <span><i className="fi-torso"> By { content.username }&nbsp;&nbsp;</i></span>
                            <br/>
                            <span><i className="fi-comments">{ content.total_attendees }attendees</i></span>
                            </p>
                            <a href="#" className="button small expanded">Join</a>
                        </div>
                    </div>  
                ))}
            </div>
        )
    }
}