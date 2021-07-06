import React, { Component } from 'react';

export class ContentFile extends Component {
    render() {
        return(
            <div>
                {/* TODO: need to change to media gallery or like */}
                {/* TODO: need to get signed version of file */}
                {this.props.files.map(file => (
                    <h4 key={file.id}>{file.source}</h4>
                ))}
            </div>
        )
    }
}