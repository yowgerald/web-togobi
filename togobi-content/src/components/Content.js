import React, { Component } from 'react';
import axios from 'axios';
import { ContentFile } from '../components/ContentFile';
import { config } from '../Constants';
import { Suggestion } from '../components/Suggestion';

const API_URL = config.url.API_URL;

export class Content extends Component {
    constructor() {
        super();
        this.state = {
            q: '',
            contents: [],
        };
    }

    async getContents(query = null) {
        await axios.get(API_URL+'/contents',
            {
                params: {
                    q: query
                }
            }).then(response => {
                this.setState({ contents: response.data })
            })
            .catch(error => {
                console.log(error);
            });
    }

    handleUpdateQuery(e) {
        this.setState({
            q: e.target.value
        });
    }

    handleSearch(query) {
        this.getContents(query);
    }

    componentDidMount() {
        this.getContents();
    }

    render() {
        return [
            <div key="content-list" className="large-6 columns">
                <div className="row column">
			    	<h4 className="text-center">LATEST</h4>
		  	    </div>
                <div className="row">
                    <div className="small-9 columns">
                        <input name="q" type="text" onChange={(e) => this.handleUpdateQuery(e)}/>
                    </div>
                    <div className="small-3 columns">
                      <input type="submit" className="button expanded" defaultValue="Search" onClick={() => this.handleSearch(this.state.q)}/>
                    </div>
                </div>
                <a href="/content/add" className="button ffab">Add Something</a>
                {this.state.contents.map(content => (
                    <div className="card" key={content.id}>
                        {/* TODO: put hrefs value */}
                        <ContentFile content={content.id}/>
                        <div className="card-section">
                            <h4><a href="#">{content.title}</a></h4>
                            <p>
                            <span>{ content.description }</span>
                            <br/>
                            <span><i className="fi-calendar">{ content.target_date } &nbsp;&nbsp;</i></span>
                            <br/>
                            <span><i className="fi-torso"> By { content.username }&nbsp;&nbsp;</i></span>
                            <br/>
                            <span><i className="fi-comments">{ content.total_attendees } attendees</i></span>
                            </p>
                            <a href="#" className="button small expanded">Join</a>
                        </div>
                    </div>  
                ))}
                {/* TODO: add pagination, maybe managed by every scroll? */}
            </div>,
            <Suggestion key="suggestion"/>
        ]
    }
}