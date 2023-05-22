function login() {
    const email = document.querySelector('#login_email').value.toLowerCase();
    const password = document.querySelector('#login_password').value;

    let k = 0;
    if (email.length == 0) {
        k=1;
        document.getElementById('login_email_error').innerHTML = "Please enter registered email id";
    }
    else
        document.getElementById('login_email_error').innerHTML = '';
    if (password.length == 0) {
        k=1;
        document.getElementById('login_password_error').innerHTML = "Please enter password";
    }
    else
        document.getElementById('login_password_error').innerHTML = '';

    if(k==1)
        return false;

    const loginUrl = baseURL + 'apis/auth/login/';
    fetch(`${loginUrl}`, {
        method: "POST",
        body: JSON.stringify({ email, password }),
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
        .then(function (json) {
            console.log(json);
            if(json.message=="Login Successful"){
                // window.location = `${userBaseURL}`;
                const prev_page = localStorage.getItem("prev_page");
                if (prev_page) {
                    window.location = prev_page;
                } else {
                    window.location = userBaseURL;
                }
            }
            else if(json.message=="User account is not verified."){
                document.getElementById('incorrect_details').innerHTML = json.message;
            }
            else {
                document.getElementById('incorrect_details').innerHTML = "Incorrect Details";
            }
        });
}

function register(){
    let first_name = document.getElementById('first_name').value;
    let last_name = document.getElementById('last_name').value;
    let email_id = document.getElementById('email').value.toLowerCase();
    let phone_no = document.getElementById('phone_no').value;
    let password = document.getElementById('password').value;
    let cpassword = document.getElementById('cpassword').value;
    let terms_and_condistions = document.getElementById('terms_and_condistions').checked;
    let check=new RegExp("[a-zA-Z0-9]@[a-z]{3,}\.[a-z]{2,}","g");
    let ngo_or_donor;
    let k = 0;
    if (document.querySelector('[name="ngo_or_donor"]:checked')) ngo_or_donor = document.querySelector('[name="ngo_or_donor"]:checked').value;
    else {
        k = 1;
        document.getElementById('ngo_or_donor_error').innerHTML = 'Please select a user type';
    }
    
    if (first_name.length == 0) {
        k=1;
        document.getElementById('first_name_error').innerHTML = "Please enter first name";
    }
    else
        document.getElementById('first_name_error').innerHTML = '';
    if (last_name.length == 0) {
        k=1;
        document.getElementById('last_name_error').innerHTML = "Please enter last name";
    }
    else
        document.getElementById('last_name_error').innerHTML = '';
    if (email_id.length == 0) {
        k=1;
        document.getElementById('email_error').innerHTML = "Please enter email id";
    }
    else if(!email_id.match(check)) {
        k=1;
        document.getElementById('email_error').innerHTML = "Please enter valid mail id";
    }
    else
        document.getElementById('email_error').innerHTML = '';
    if (phone_no.length == 0) {
        k=1;
        document.getElementById('phone_no_error').innerHTML = "Please enter phone number";
    }
    else if(phone_no.length != 10) {
        k=1;
        document.getElementById('phone_no_error').innerHTML = "Please enter 10 numbers";
    }
    else
        document.getElementById('phone_no_error').innerHTML = '';
    if (password.length == 0) {
        k=1;
        document.getElementById('password_error').innerHTML = "Please enter password";
    }
    else
        document.getElementById('password_error').innerHTML = '';
    if (cpassword.length == 0) {
        k=1;
        document.getElementById('cpassword_error').innerHTML = "Please enter confirm password";
    }

    else if(password != cpassword) {
        k=1;
        document.getElementById('cpassword_error').innerHTML = "Password and confirm password should be same";
    }
    else
        document.getElementById('cpassword_error').innerHTML = '';

    if(!terms_and_condistions) {
        k = 1;
        document.getElementById('terms_and_condistions_error').innerHTML = 'Please select on terms and conditions';
    }
    else
       document.getElementById('terms_and_condistions_error').innerHTML = '';
    if(k==1)
    return false;

    const registerUrl = baseURL + 'apis/auth/signup/';
    document.querySelector('#registerButton').disabled = true;
    fetch(`${registerUrl}`, {
        method: "POST",
        body: JSON.stringify({ email: email_id, first_name, last_name, phone_number:phone_no, password, user_type: ngo_or_donor }),
        crossDomain: true,
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        },
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (json) {
            console.log(json);
            if(json.message && json.message.includes('Verification mail has been sent')){
                new sweetAlert("Congratulations", json.message, "success")
                .then(function(){
                    window.location = `${userBaseURL}login/`;
                });
            } else if (json.email) {
                document.getElementById('email_error').innerHTML = json.email[0];
            } else if (json.phone_number) {
                document.getElementById('phone_no_error').innerHTML = json.phone_number[0];
            } else if (json.password) {
                document.getElementById('password_error').innerHTML = json.password[0]
            } else {
                document.getElementById('terms_and_condistions_error').innerHTML = 'Something happened wrong, please try later';
            }
            document.querySelector('#registerButton').disabled = false;
        });

    return false;
}


function verifyRestCode() {
    console.log(code);
    if (code.length == 0) {
        new sweetAlert("Sorry", "Invalid code", "error")
        .then(function(){
            window.location = userBaseURL +'forgot-password/';
        });
    }
    fetch(`${baseURL}apis/auth/password/reset/verify/${code}/`, {
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
        if (response.message == 'Invalid Request' || response.detail == 'Invalid Token') {
            new sweetAlert("Success", response.message, "error")
            .then(function(){
                 window.location = userBaseURL +'forgot-password/';
            });
        } else {
            new sweetAlert("Success", response.message, "success")
            .then(function(){
                document.querySelector('.boxed_wrapper').style.display = 'block';
            });
        }
    });

}
function resetPass(){
    let password = document.getElementById('password').value;
    let confirm_password = document.getElementById('confirm_password').value;

    var flag=0;
    if (password.length == 0) {
        flag=1;
        document.getElementById('password_error').innerHTML = "Please enter password";
    } else
        document.getElementById('password_error').innerHTML = '';

    if(password!=confirm_password){
        document.getElementById('confirm_password_error').innerHTML = "Passwords didn't match";
        flag=1;
    } else{
        document.getElementById('confirm_password_error').innerHTML = '';
    }
    
    if (flag == 1) return false;
    if(flag==0){
        fetch(`${baseURL}apis/auth/password/reset/verified/${code}/`, {
            method: "POST",
            body: JSON.stringify({ password: password }),
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
            if (response.message == 'Invalid Request') {
                new sweetAlert("Success", response.message, "error")
                .then(function(){
                     window.location = userBaseURL +'forgot-password/';
                });
            } else {
                new sweetAlert("Success", response.message, "success")
                .then(function(){
                    window.location = userBaseURL +'login/';
                });
            }
        });
    }
    return false;
}

function forgotPassword(){
    let email_id = document.getElementById('email').value;
    let check=new RegExp("[a-zA-Z0-9]@[a-z]{3,}\.[a-z]{2,}","g");
    console.log(email_id);
    if (!email_id) {
        document.getElementById('email_error').innerHTML = "Please enter valid email id";
        return false;
    } else if(!email_id.match(check)) {
        document.getElementById('email_error').innerHTML = "Please enter valid mail id";
        return false;
    } else {
        document.getElementById('email_error').innerHTML = ""
    }

    document.getElementById('forgotPass').disabled = true;
    fetch(`${baseURL}apis/auth/password/reset/request/${email_id}/`, {
        method: "GET",
        crossDomain: true,
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        },
    })
    .then(function (response) {
        return response.json();
    })
    .then(function(response){
        console.log(response);
        if (response.message == 'Password reset mail sent successfully') {
            new sweetAlert("Success", response.message, "success")
                .then(function(){
                    window.location = userBaseURL;
                });
        } else {
            new sweetAlert("Sorry", response.message, "error")
                .then(function(){
                    window.location = userBaseURL +'forgot-password/';
                });
        }
        document.getElementById('forgotPass').disabled = false;
    })

    return false;

}

function verifyMail() {
    if (code.length == 0) {
        alert("invalid code");
        return false;
    }

    fetch(`${baseURL}apis/auth/signup/verify/${code}/`, {
        method: "POST",
        crossDomain: true,
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        },
    })
    .then(function (response) {
        return response.json();
    })
    .then(function(response){
        console.log(response);
        if (response.message == 'User verified successfully') {
            new sweetAlert("Congratulations", response.message, "success")
                .then(function(){
                    window.location = `${userBaseURL}login/`;
                });
        } else {
            new sweetAlert("Sorry", response.message, "error")
                .then(function(){
                    window.location = `${userBaseURL}register/`;
                });
        }
//        alert(response.message);
    })

}

function logout() {
    fetch(`${baseURL}apis/auth/logout/`, {
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
            
            window.location = `${userBaseURL}`;
        });
}

function changePass(){
    let old_password = document.getElementById('old_password').value;
    let password = document.getElementById('password').value;
    let confirm_password = document.getElementById('confirm_password').value;

    var flag=0;
    if (old_password.length == 0) {
        flag=1;
        document.getElementById('old_password_error').innerHTML = "Please enter old password";
    } else document.getElementById('old_password_error').innerHTML = '';

    if (password.length == 0) {
        flag=1;
        document.getElementById('password_error').innerHTML = "Please enter password";
    } else if (password == old_password) {
    //    flag=1;
    //     document.getElementById('password_error').innerHTML = "New password should not be old password";
    } else
        document.getElementById('password_error').innerHTML = '';

    if(password!=confirm_password){
        document.getElementById('confirm_password_error').innerHTML = "Passwords didn't match";
        flag=1;
    }
    else{
        document.getElementById('confirm_password_error').innerHTML = '';
    }

    if(flag==0){
        document.getElementById('changePassword').disabled = true;
        fetch(`${baseURL}apis/auth/password/change/`, {
            method: "POST",
            body: JSON.stringify({ old_password, new_password: password }),
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
            console.log(response);
            if (response.message == 'Invalid Old Password') {
                document.getElementById('old_password_error').innerHTML = response.message;
                document.getElementById('changePassword').disabled = false;
            } else if (response.message == 'Password reset Successful') {
                new sweetAlert("Congratulations", response.message, "success")
                .then(function(){
                    window.location = userBaseURL;
                });

            } else {
                document.getElementById('confirm_password_error').innerHTML = 'Something happened wrong, please try later';
                document.getElementById('changePassword').disabled = false;
            }
            
            document.getElementById('changePassword').disabled = false;
        })
    }
    return false;
}