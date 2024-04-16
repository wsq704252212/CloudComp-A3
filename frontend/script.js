var apigClient;

window.onload = function () {
    apigClient = apigClientFactory.newClient();

    document.getElementById('search-button').onclick = function () {
        var query = document.getElementById('search-query').value;
        search(query);
    };

    document.getElementById('upload-form').onsubmit = function (event) {
        event.preventDefault();
        var photo = document.getElementById('photo-upload').files[0];
        var labels = document.getElementById('custom-labels').value.trim().split(',');
        upload(photo, labels);
    }
}

function search(query) {
    var params = {
        'q': query.trim()
    };
    var body = {};
    var additionalParams = {
        headers: {},
        queryParams: {}
    };

    apigClient.searchGet(params, body, additionalParams)
        .then(function (result) {
            console.log('Search results:', result);
            displayPhotos(result);
        })
        .catch(function (result) {
            console.error('Error searching photos:', result);
        });
}

function upload(photo, labels) {
    // console.log(photo)
    // var params = {
    //     'filename': photo.name
    // };
    // var body = photo;
    // var additionalParams = {
    //     headers: {
    //         'Content-Type': photo.type,
    //         'x-amz-meta-customLabels': labels
    //     }
    // };

    // apigClient.uploadFilenamePut(params, body, additionalParams)
    //     .then(function (result) {
    //         console.log('Photo uploaded:', result);
    //     })
    //     .catch(function (result) {
    //         console.error('Error uploading photo:', result);
    //     });

    xhr = new XMLHttpRequest();
    xhr.open('PUT', 'https://h57p765qx6.execute-api.us-east-1.amazonaws.com/dev/upload/' + photo.name);
    xhr.setRequestHeader('Content-Type', photo.type);
    xhr.setRequestHeader('x-amz-meta-customLabels', labels);
    xhr.send(photo);
}

function displayPhotos(result) {
    var imageContainer = document.querySelector('.image-container');
    imageContainer.innerHTML = '';

    photoName = result['data']['photoName']
    photoUrl = result['data']['photoUrl']
    var imgElement = document.createElement('img');
    imgElement.src = photoUrl;
    imgElement.alt = photoName;
    imgElement.classList.add('photo');
    imageContainer.appendChild(imgElement);
}