const prod = {
    url: {
        API_URL: '',
    }
};

const dev = {
    url: {
        API_URL: 'http://localhost:8000'
    }
};

export const config = process.env.NODE_ENV === 'development' ? dev : prod;
export const fileType = {
    IMAGE: 'Image',
    VIDEO: 'Video'
}
export const uploadStatus = {
    IN_QUEUE: 'Waiting',
    IN_PROGRESS: 'Uploading',
    DONE: 'Finished', 

}