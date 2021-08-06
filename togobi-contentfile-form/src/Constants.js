const prod = {
    API_URL: '',
};

const dev = {
    API_URL: 'http://localhost:8000',
};

export const config = process.env.NODE_ENV === 'development' ? dev : prod;
export const fileType = {
    IMAGE: 'Image',
    VIDEO: 'Video'
};
export const uploadStatus = {
    IN_QUEUE: 'Waiting',
    IN_PROGRESS: 'Uploading',
    DONE: 'Finished', 
};
export const formMode = {
    ADD: 0,
    EDIT: 1,
};
const EL_CSRF =  document.querySelector("input[name='csrfmiddlewaretoken'");
export const csrftoken = EL_CSRF !== null ? EL_CSRF.value : null;

export const appendScript = (scriptToAppend, isAsync = false) => {
    const script = document.createElement("script");
    script.src = scriptToAppend;
    script.async = isAsync;
    document.body.appendChild(script);
};
export const removeScript = (scriptToremove) => {
    let allsuspects=document.getElementsByTagName("script");
    for (let i=allsuspects.length; i>=0; i--){
        if (allsuspects[i] && allsuspects[i].getAttribute("src") !== null 
        && allsuspects[i].getAttribute("src").indexOf(`${scriptToremove}`) !== -1 ){
           allsuspects[i].parentNode.removeChild(allsuspects[i])
        }    
    }
}