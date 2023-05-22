let active_page;
function postOptions(url, data) {
    const options = {
        url,
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            "Access-Control-Allow-Methods": "GET, POST, DELETE, PUT, PATCH"
        },
        data,
    };
    return options;
}

function getOptions(url) {
    const options = {
        url,
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            "Access-Control-Allow-Methods": "GET, POST, DELETE, PUT, PATCH"
        }
    };
    return options; 
}

function putOptions(url, data) {
    const options = {
        url,
        method: "PUT",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            "Access-Control-Allow-Methods": "GET, POST, DELETE, PUT, PATCH"
        },
        data,
    };
    return options;
}

function deleteOptions(url) {
    const options = {
        url,
        method: "DELETE",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            "Access-Control-Allow-Methods": "GET, POST, DELETE, PUT, PATCH"
        }
    };
    return options; 
}

function setInitialPage() {
    if (active_page && active_page != 'login' && active_page != 'register' && active_page != 'forgotpassword' && active_page != 'resetpassword') {
        console.log(window.location.href);
        localStorage.setItem('prev_page', window.location.href);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    setInitialPage();
})