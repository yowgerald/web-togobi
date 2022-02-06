import React, { useState } from "react";
import { BasicInputs } from "./fields/BasicInputs";
import { initContentDetails } from "../../Initializers";

export const Create = () => {

    const [contentDetails, setContentDetails] = useState(initContentDetails);

    const handleStatus = e => {
        let c_ds = {...contentDetails}
        c_ds.is_active = !contentDetails.is_active;
        setContentDetails(c_ds);
    }

    const props = { contentDetails, handleStatus };

    return (
        <React.Fragment>
            <div className="row">
                <div className="columns small-12 large-6">
                    <BasicInputs {...props}/>
                </div>
                <div className="columns small-12 large-6">
                    {/* TODO: may need to add note about saving the content first. */}
                </div>
            </div>
        </React.Fragment>
    )
}