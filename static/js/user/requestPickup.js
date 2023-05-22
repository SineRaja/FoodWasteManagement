function requestPickup() {
    if (!checkTokenExists()) {
        return false;
    }
    const brief_desc = document.querySelector('#brief_desc').value;
    const company_name = document.querySelector('#company_name').value;
    const company_type = document.querySelector('#company_type').value;
    const address = document.querySelector('#address').value;
    const pincode = document.querySelector('#pincode').value;
    const quantity = document.querySelector('#quantity').value;
    const date = document.querySelector('#datepicker').value;
    const time = document.querySelector('#time').value;
    // console.log(brief_desc, address, pincode, date, time, company_name, company_type);

    document.querySelector('#res_message').innerHTML = "";
    let error = false;
    if (brief_desc.length == 0) {
        error = true;
        document.querySelector('#brief_desc_error').innerHTML = "Please enter a description";
        document.querySelector('#email').style.marginTop = "10px";
    } else {
        document.querySelector('#brief_desc_error').innerHTML = "";
    }

    if (company_name.length == 0) {
        error = true;
        document.querySelector('#company_name_error').innerHTML = "Please enter a company name";
    } else {
        document.querySelector('#company_name_error').innerHTML = "";
    }

    if (company_type.length == 0) {
        error = true;
        document.querySelector('#company_type_error').innerHTML = "Please select company type";
    } else {
        document.querySelector('#company_type_error').innerHTML = "";
    }
     
    if (pincode.length == 0) {
        error = true;
        document.querySelector('#pincode_error').innerHTML = "Please enter pincode";
    } else {
        document.querySelector('#pincode_error').innerHTML = "";
    }

    if (address.length == 0) {
        error = true;
        document.querySelector('#address_error').innerHTML = "Please enter address";
    } else {
        document.querySelector('#address_error').innerHTML = "";
    }

    if (!quantity) {
        error = true;
        document.querySelector('#quantity_error').innerHTML = "Please enter quantity";
    } else {
        document.querySelector('#quantity_error').innerHTML = "";
    }

    if (date.length == 0) {
        error = true;
        document.querySelector('#datepicker_error').innerHTML = "Please select a date";
    } else {
        document.querySelector('#datepicker_error').innerHTML = "";
    }

    if (time.length == 0) {
        error = true;
        document.querySelector('#time_error').innerHTML = "Please select a time";
    } else {
        document.querySelector('#time_error').innerHTML = "";
    }

    if (error) return false;

    
    document.getElementById('request-a-pickup-btn').disabled = true;
    const date_split = date.split("/")
    let original_date = date_split[2]+"-"+date_split[0]+"-"+date_split[1]; 
    const meridian = time.split(" ")[1];
    const time_split_with_colon = time.split(" ")[0].split(":");
    if (meridian == 'PM') {
        const time_with_meridian = parseInt(time_split_with_colon[0]) + 12;
        original_date += `T${time_with_meridian}:${time_split_with_colon[1]}:00`;
    } else {
        original_date += `T${time_split_with_colon[0]}:${time_split_with_colon[1]}:00`;
    }

    const data = {
        company_name,
        company_type,
        food_type: "COOKED",
        food_description: brief_desc,
        address: {
            name: user_details.first_name,
            phone_number: user_details.phone_number,
            pincode,
            address_line: address,
            extend_address: null,
            landmark: null,
            city: "Leicester",
            state: "Le2 1xp",
            country: "England",
            latitude: null,
            longitude: null
        },
        pickup_date_time: original_date,
        quantity
    }

    const options = postOptions(`${baseURL}apis/food_request/request/`, data);
    axios(options)
    .then(function (response) {
        console.log(response);
        document.getElementById('request-a-pickup-btn').disabled = false;
        document.querySelector('#brief_desc').value = "";
        document.querySelector('#company_name').value = "";
        document.querySelector('#company_type').value = "";
        document.querySelector('#address').value = "";
        document.querySelector('#pincode').value = "";
        document.querySelector('#datepicker').value = "";
        document.querySelector('#time').value = "";
        document.querySelector('#res_message').innerHTML = "Thanks for helping, will contact you soon.";
    })
    .catch(function (response){
        console.log(response);
        document.getElementById('request-a-pickup-btn').disabled = false;
        document.querySelector('#res_message').innerHTML = "Something happened wrong, Please try later.";
        document.querySelector('#res_message').style.color = 'red';
    })

    document.getElementById('request-a-pickup-btn').disabled = false;
    return false;
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
        const email = document.getElementById('email');
        last_name.value = response.last_name;
        last_name.disabled = true;
        first_name.value = response.first_name;
        first_name.disabled = true;
        email.value = response.email;
        email.disabled = true;
      });
}

document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token');
    if (token)  fillUserDetails();
})