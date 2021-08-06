import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { config, csrftoken, formMode, appendScript, removeScript } from '../../Constants';

export const Step1 = ({ mode, content }) => {
    const initialDetails = {
        title: '',
        description: '',
        tags: '',
        target_date: null,
        is_active: false,
    };

    const [contentDetails, setContentDetails] = useState(initialDetails);

    const initMapUrl = '/static/gmap/map_api.js';
    const mapApiSource = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyD0N-EiHuwDqA2WslFWqEteBGwokddQ_SE&libraries=places&callback=initMap';

    const handleStatus = e => {
        let c_ds = {...contentDetails}
        c_ds.is_active = !contentDetails.is_active;
        setContentDetails(c_ds);
    }

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
        if (mode === formMode.EDIT) {
            getContentDetails();
        }
        appendScript(initMapUrl);
        appendScript(mapApiSource, true);
        return () => {
            removeScript(initMapUrl);
            removeScript(initMapUrl);
        }
    }, [mode, getContentDetails]);

    return (
        <React.Fragment>
            <p>
                <label htmlFor="id_title">Title:</label>
                <input type="text" name="title" defaultValue={contentDetails.title} maxLength="200" required="" id="id_title"></input>
            </p>
            <p>
                <label htmlFor="id_description">Description:</label>
                <textarea name="description" defaultValue={contentDetails.description} cols="20" rows="5" maxLength="200" required="" id="id_description"></textarea>
            </p>
            <p>
                <label htmlFor="id_tags">Tags:</label>
                <input type="text" name="tags" defaultValue={contentDetails.tags} maxLength="200" required="" id="id_tags"></input>
            </p>
            <p>
                <label htmlFor="id_target_date">Target date:</label>
                <input type="datetime-local" name="target_date" defaultValue={contentDetails.target_date} required="" id="id_target_date"></input>
            </p>
            <p>
                <label htmlFor="id_is_active">Active:</label>
                <input type="checkbox" name="is_active" id="id_is_active" checked={contentDetails.is_active || mode === formMode.ADD} onChange={() => handleStatus()}></input>
            </p>
            <p>
                <label htmlFor="id_location">Location:</label>
                <input type="text" name="location" required="" id="id_location"></input>
            </p>
        </React.Fragment>
    )
}
