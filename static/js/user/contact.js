function contactUs() {
    let name = document.querySelector('#name').value;
    let email = document.querySelector('#email').value; 
    let phone_no = document.querySelector('#phone').value; 
    let subject = document.querySelector('#subject').value; 
    let message = document.querySelector('#message').value;  
    let check=new RegExp("[a-zA-Z0-9]@[a-z]{3,}\.[a-z]{2,}","g");

    let is_valid = true;
    if (!name) {
        is_valid = false;
        document.querySelector('#name_error').innerHTML =  "Please enter a name.";
    } else {
        document.querySelector('#name_error').innerHTML =  "";
    }

    if (!email) {
        is_valid = false;
        document.querySelector('#email_error').innerHTML =  "Please enter an email address.";
    } else if(!email.match(check)) { 
        is_valid = false;
        document.querySelector('#email_error').innerHTML =  "Please enter valid email address.";
    } else {
        document.querySelector('#email_error').innerHTML =  ""; 
    }
    
    if (!phone_no) {
        is_valid = false;
        document.querySelector('#phone_error').innerHTML =  "Please enter a phone number.";
    } else if (phone_no.length != 10) {
        is_valid = false;
        document.querySelector('#phone_error').innerHTML =  "Phone number must be at least 10 characters long.";
    } else {
        document.querySelector('#phone_error').innerHTML =  "";
    }

    if (!subject) {
        is_valid = false;
        document.querySelector('#subject_error').innerHTML =  "Please enter a subject.";
    } else {
        document.querySelector('#subject_error').innerHTML =  "";
    }

    if (!message) {
        is_valid = false;
        document.querySelector('#message_error').innerHTML =  "Please enter a message.";
    } else {
        document.querySelector('#message_error').innerHTML =  "";
    }

    if (!is_valid) {
        return false;
    }

    if (name && email && phone_no && subject && message) {
        const data = {
            name,
            email,
            phone_no,
            subject,
            message
        }

        document.getElementById('contact-btn-submit').disabled = true;
        const options = postOptions(`${baseURL}apis/review/contact_us/`, data);
        axios(options)
        .then(function (response) {
            // console.log("contact us response",response.data);
            let res_message = document.getElementById('res_message');
            if (response.data.id) {
                document.querySelector('#name').value = "";
                document.querySelector('#email').value = "";
                document.querySelector('#phone').value = "";
                document.querySelector('#subject').value = "";
                document.querySelector('#message').value = "";
                res_message.innerHTML = "Thanks for your feedback";
                res_message.style.color = "green";
            } else {
                res_message.innerHTML = "Sorry, something went wrong. Please try again later";
            }

            document.getElementById('contact-btn-submit').disabled = false;
        })
        .catch(function (response){
            console.log(response);
        })
    }
    // return false;
}