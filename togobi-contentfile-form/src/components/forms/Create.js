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

    return <BasicInputs {...props}/>
}