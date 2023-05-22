function getNGORequests() {
    const options = getOptions(`${baseURL}apis/food_request/requests/active/`);
    axios(options)
    .then(function (response) {
        console.log('pending',response);
        let my_request_str = ``;
        if (response.data.results.length == 0) my_request_str = `<h3>No results found</h3>`;
        response.data.results.forEach(req => {
            let address = `${req.address.address_line}, ${req.address.city}, ${req.address.state}, ${req.address.country}, ${req.address.pincode}, ${req.address.phone_number}`;
            my_request_str +=  `
                <div class="col-12">
                    <div class="card">
                        <h3>${req.created_by.name}</h3>
                        <div class="row">
                            <div class="col-12 col-md-7">
                                Company Name: <strong>${req.company_name}</strong><br>
                                Email Id: <strong>${req.created_by.email}</strong><br>
                            </div>
                            <div class="col-12 col-md-5">
                                Company Type: <strong>${req.company_type}</strong><br>
                                Food Type: <strong>${req.food_type}</strong><br>
                            </div>
                            <div class="col-12">
                                Pickup Date: <strong>${req.pickup_date_time.substr(0,10)} ${req.pickup_date_time.substr(11,17)}</strong><br>
                                Total Quantity: <strong>${req.quantity}</strong><br>
                                Address: <b>${address}</b><br>
                                Description: <b>${req.food_description}</b>
                            </div>
                            <br>
                            <div class="col-12">
                                <button class="btn btn-success" id="accept" data-toggle="modal" data-target="#acceptModal" onclick="acceptId('${req.id}')">Accept</button>
                                <a href="${baseURL}issue/${req.id}/" class="btn btn-info" id="raise_an_issue">Raise an issue</a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        document.querySelector('#my-requests').innerHTML = my_request_str;
    })
    .catch(function (response){
        console.log(response);
    })

    const acceptedOptions = getOptions(`${baseURL}apis/food_request/requests/my/accepted/`);
    axios(acceptedOptions)
    .then(function (response) {
        console.log('accepted',response);
        let my_request_str = ``;
        if (response.data.results.length !== 0) my_request_str = `<h1 style="margin: 20px">Accepted Requests</h1>`;

        response.data.results.forEach(req => {
            let address = `${req.address.address_line}, ${req.address.city}, ${req.address.state}, ${req.address.country}, ${req.address.pincode}, ${req.address.phone_number}`;
            my_request_str +=  `
                <div class="col-12">
                    <div class="card">
                        <h3>${req.created_by.name}</h3>
                        <div class="row">
                            <div class="col-12 col-md-7">
                                Company Name: <strong>${req.company_name}</strong><br>
                                Email Id: <strong>${req.created_by.email}</strong><br>
                            </div>
                            <div class="col-12 col-md-5">
                                Company Type: <strong>${req.company_type}</strong><br>
                                Food Type: <strong>${req.food_type}</strong><br>
                            </div>
                            <div class="col-12">
                                Pickup Date: <strong>${req.pickup_date_time.substr(0,10)} ${req.pickup_date_time.substr(11,17)}</strong><br>
                                Total Quantity: <strong>${req.quantity}</strong><br>
                                Address: <b>${address}</b><br>
                                Description: <b>${req.food_description}</b>
                            </div>
                            <br>
                            <div class="col-12">
                                <a href="${baseURL}issue/${req.id}/" class="btn btn-info" id="raise_an_issue">Raise an issue</a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        // <button class="btn btn-danger" id="reject" data-toggle="modal" data-target="#rejectModal"  onclick="rejectId('${req.id}')">Reject</button>
                                

        document.querySelector('#accepted-requests').innerHTML = my_request_str;
    })
    .catch(function (response){
        console.log(response);
    })
}


function getMyRequests() {
    const options = getOptions(`${baseURL}apis/food_request/requests/my/`);
    axios(options)
    .then(function (response) {
        console.log(response);
        let my_request_str = ``;
        if (response.data.results.length == 0) my_request_str = `<h1>No results found</h1>`;
        response.data.results.forEach(req => {
            let address = `${req.address.address_line}, ${req.address.city}, ${req.address.state}, ${req.address.country}, ${req.address.pincode}, ${req.address.phone_number}`;
            
            let status_button = ``;
            if (req.request_status === 'COMPLETED') {
                status_button = `
                    <button class="btn btn-success" id="reject"   disabled>Completed</button>
                `;
            } else if (req.request_status === 'CANCELLED') {
                status_button = `
                    <button class="btn btn-warning" id="reject" disabled>Cancelled</button>
                `;
            } else {
                status_button = `
                    <button class="btn btn-danger" id="reject" data-toggle="modal" data-target="#deleteModal"  onclick="deleteId('${req.id}')">Delete</button>
                `;
            }

            status_button += `<a href="${baseURL}issue/${req.id}/" class="btn btn-info" id="raise_an_issue">Raise an issue</a>`;
            my_request_str +=  `
                <div class="col-12">
                    <div class="card">
                        <h3>${req.created_by.name}</h3>
                        <div class="row">
                            <div class="col-12 col-md-7">
                                Company Name: <strong>${req.company_name}</strong><br>
                                Email Id: <strong>${req.created_by.email}</strong><br>
                            </div>
                            <div class="col-12 col-md-5">
                                Company Type: <strong>${req.company_type}</strong><br>
                                Food Type: <strong>${req.food_type}</strong><br>
                            </div>
                            <div class="col-12">
                                Pickup Date: <strong>${req.pickup_date_time.substr(0,10)} ${req.pickup_date_time.substr(11,17)}</strong><br>
                                Total Quantity: <strong>${req.quantity}</strong><br>
                                Address: <b>${address}</b><br>
                                Description: <b>${req.food_description}</b>
                            </div>
                            <br>
                            <div class="col-12">
                                ${status_button}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        document.querySelector('#my-requests').innerHTML = my_request_str;
    })
    .catch(function (response){
        console.log(response);
    })
}

let accept_request_id, reject_request_id, delete_request_id;
function acceptId(request_id) {
    accept_request_id = request_id;
}

function rejectId(request_id) {
    reject_request_id = request_id;
}

function deleteId(request_id) {
    delete_request_id = request_id;
}

function accept() {
    if (!accept_request_id) return;
    const options = postOptions(`${baseURL}apis/food_request/request/accept/${accept_request_id}/`, {});
    axios(options)
    .then(function (response) {
        console.log(response);
        toastMixin.fire({
            animation: true,
            title: 'Successfully Accepted'
          });
        document.querySelector('#acceptModalClose').click();
        const user_details = JSON.parse(localStorage.getItem('user_details'));
        if (user_details.user_type == 'NGO') getNGORequests();
        else getMyRequests();
    })
    .catch(function (response){
        console.log(response);
        alert("something went wrong");
    })
}

function reject() {
    if (!reject_request_id) return;
    const options = postOptions(`${baseURL}apis/food_request/request/cancel/${reject_request_id}/`, {});
    axios(options)
    .then(function (response) {
        console.log(response);
        toastMixin.fire({
            animation: true,
            title: 'Successfully Rejected'
          });
        document.querySelector('#rejectModalClose').click();
        const user_details = JSON.parse(localStorage.getItem('user_details'));
        if (user_details.user_type == 'NGO') getNGORequests();
        else getMyRequests();
    })
    .catch(function (response){
        console.log(response);
        alert("something went wrong");
    })
}

function deleteRequest() {
    if (!delete_request_id) return;
    const options = postOptions(`${baseURL}apis/food_request/request/cancel/${delete_request_id}/`, {});
    axios(options)
    .then(function (response) {
        console.log(response);
        toastMixin.fire({
            animation: true,
            title: 'Successfully Deleted'
          });
        document.querySelector('#deleteModalClose').click();
        const user_details = JSON.parse(localStorage.getItem('user_details'));
        if (user_details.user_type == 'NGO') getNGORequests();
        else getMyRequests();
    })
    .catch(function (response){
        console.log(response);
        alert("something went wrong");
    })
}

document.addEventListener('DOMContentLoaded', () => {
    const user_details = JSON.parse(localStorage.getItem('user_details'));
    if (user_details.user_type == 'NGO') getNGORequests();
    else getMyRequests();
})