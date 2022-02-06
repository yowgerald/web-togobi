import React, { useState } from "react";
import { Create } from "./forms/Create";
import { Edit } from "./forms/Edit";

export const ContentForm = () => {
    const container = document.getElementById('root');
    let [content, ] = useState(container.getAttribute('content') !== null ? parseInt(container.getAttribute('content')) : null);

    if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
        content = 1;
    }

    const props = { content };

    return (
        <React.Fragment>
            { content !== null ? <Edit {...props}/> : <Create {...props}/>}
            <button type="submit" className="secondary button float-right">Save</button>
        </React.Fragment>

    )
}