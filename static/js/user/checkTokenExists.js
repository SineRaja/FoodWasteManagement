function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
  
  function checkTokenExists() {
    const token = getCookie('token');
    if (!token) {
      window.location = `${userBaseURL}login/`;
      return false;
    }
    return true;
  }
  let user_details;
  document.addEventListener('DOMContentLoaded', () => {
    if (window.location.href == userBaseURL+ 'login/' || window.location.href == userBaseURL+ 'register/' || window.location.href == userBaseURL+ 'reset-password/') {
        if (getCookie('token')) {
            console.log("token is there");
            window.location = userBaseURL;
        }
    } else if (window.location.href == userBaseURL+ 'my-requests/' || window.location.href == userBaseURL+ 'issue/' || window.location.href.includes(userBaseURL+ 'booking/') || window.location.href.includes(userBaseURL + 'booking-invoice/') || window.location.href == userBaseURL+ 'change-password/' || window.location.href == (userBaseURL+ 'bookings/')) {
       if (!getCookie('token'))  window.location = userBaseURL + 'login/';
    }
  
  
    if (getCookie('token')) {
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
          user_details = response;
          // console.log(response);
          localStorage.setItem('user_details', JSON.stringify(user_details));

          const login_buttons = document.querySelectorAll('.login-button');
          const profile_dropdowns = document.querySelectorAll('.profile-dropdown');
          const user_names = document.querySelectorAll('#user_name');
          const user_types = document.querySelectorAll('#user_type');
  
          login_buttons.forEach(login_button => {
            login_button.classList.add('hide-content');
          });
          profile_dropdowns.forEach(profile_dropdown => {
            profile_dropdown.classList.remove('hide-content');
          });
          user_names.forEach(username => {
            username.innerHTML = response.first_name.charAt(0).toUpperCase() + response.first_name.slice(1);
          });
          user_types.forEach(type => {
            if (response.user_type == 'DONOR') type.innerHTML = ' Donor';
            else {
              type.innerHTML = ' NGO';
              const request_pick_up_btns = document.querySelectorAll('[data-action="request-pickup-btn"]');
              request_pick_up_btns.forEach(each_btn => {
                  each_btn.style.display = 'none';
              })
            }
          });
      });
  
    }
  })