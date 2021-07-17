import React, { Component } from 'react';
import { Today } from '../components/Today';
import { Top } from '../components/Top';

export class Suggestion extends Component {
    render() {
        return (
            <div className="large-6 columns">
                <aside>
                    <br/>
                    <Today/>
                    <hr/>
                    <Top/>
                </aside>
            </div>
        )
    }
}