import React, { useEffect } from 'react';
import getCookie from '../helpers/csrfToken';


const CSRFToken = (props) => {
    var csrftoken = getCookie('csrftoken');
    useEffect(()=> {
        props.setToken(csrftoken);
    }, [])
    return (
        <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
    );
};
export default CSRFToken;