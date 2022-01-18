import React, { useEffect, useState, useCallback } from "react";
import { BasicInputs } from "./fields/BasicInputs";
import axios from 'axios';
import { config, csrftoken } from '../../Constants';
import { initContentDetails } from "../../Initializers";

export const Edit = ({ content, }) => {

    const [contentDetails, setContentDetails] = useState(initContentDetails);

    const getContentDetails = useCallback(
        () => {
            axios.get(config.API_URL + '/content/' + content, {
                headers: {
                    'X-CSRFToken': csrftoken
                },
            }).then(response => {
                setContentDetails(response.data.result)
            }).catch(error => {
                console.log(error);
                // TODO: may need to return something.
            });
        }, [content])

    useEffect(() => {
        getContentDetails();
    }, [])

    const handleStatus = e => {
        let c_ds = {...contentDetails}
        c_ds.is_active = !contentDetails.is_active;
        setContentDetails(c_ds);
    }

    const props = { contentDetails, handleStatus };

    return <BasicInputs {... props}/>
}