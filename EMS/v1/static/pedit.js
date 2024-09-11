document.addEventListener('DOMContentLoaded', function() {
let psave = document.getElementById('psave');

let image = document.getElementById('image-upload');
let full_name = document.getElementById('name');
let email = document.getElementById('email');
let username = document.getElementById('username');
let birth_date = document.getElementById('birth_date');
let timer = document.getElementById("timer")
timer.style.display = "none"

psave.addEventListener('click', function(event) {

    event.preventDefault();
    psave.style.display = "none";
    timer.style.display = "block"
    let user = event.target.getAttribute("data-username");
    setTimeout(function() {
        window.location.href = `/v1/editUser/${username.value}`;
    },2000)
 

    const formData = new FormData();
    if (image.files[0]) {
        formData.append('image', image.files[0]);
    }
    if (full_name.value) {
        formData.append('full_name', full_name.value);
       
    }
    if (email.value) {
        formData.append('email', email.value);
    }
    if (username.value) {
        formData.append('username', username.value);
    }
    if (birth_date.value) {
        formData.append('birth_date', birth_date.value);
    }

    fetch(`../editUser/${user}`, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(err => {
        console.log(err);
    });
});
})