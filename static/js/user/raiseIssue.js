function raiseIssue() {
    if (!checkTokenExists()) {
        return false;
    }
    const issue_desc = document.querySelector('#issue_desc').value;
    const issue_title = document.querySelector('#issue_title').value;
    const issue_type = document.querySelector('#issue_type').value;

    let error = false;
    if (issue_desc.length == 0) {
        error = true;
        document.querySelector('#issue_desc_error').innerHTML = "Please enter a issue description";
    } else {
        document.querySelector('#issue_desc_error').innerHTML = "";
    }

    if (issue_title.length == 0) {
        error = true;
        document.querySelector('#issue_title_error').innerHTML = "Please enter a issue title";
    } else {
        document.querySelector('#issue_title_error').innerHTML = "";
    }

    if (issue_type.length == 0) {
        error = true;
        document.querySelector('#issue_type_error').innerHTML = "Please enter a issue type";
    } else {
        document.querySelector('#issue_type_error').innerHTML = "";
    }

    if (error) return;

    document.getElementById('raise-an-issue-btn').disabled = true;
    const data = {
        issue_title,
        issue_type,
        issue_description: issue_desc,
        request: request_id
    }

    const options = postOptions(`${baseURL}apis/issues/`, data);
    axios(options)
    .then(function (response) {
        console.log(response);
        document.querySelector('#res_message').innerHTML = "Thanks for pointing the issue, we will try to resolve ASAP.";
        document.querySelector('#issue_desc').value = '';
        document.querySelector('#issue_title').value = '';
        document.querySelector('#issue_type').value = '';
    })
    .catch(function (response){
        console.log(response);
        document.querySelector('#res_message').innerHTML = "Something went wrong please try again later.";
        document.querySelector('#res_message').style.color = "red";
    })
}

function fillUserDetails() {
    fetch(`${baseURL}apis/auth/user/me/`, {
        method: "GET",
        crossDomain: true,
        credentials: 'include',
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        },
        xhrFields: {
          withCredentials: true
        },
      })
      .then(function (response) {
          return response.json();
      })
      .then(function(response){
        console.log("fillUserDetails",response);
        const first_name = document.getElementById('first_name');
        const last_name = document.getElementById('last_name');
        last_name.value = response.last_name;
        last_name.disabled = true;
        first_name.value = response.first_name;
        first_name.disabled = true;
      });
}

document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token');
    if (token)  fillUserDetails();
})