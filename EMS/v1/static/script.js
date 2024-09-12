
document.addEventListener('DOMContentLoaded', function() {
    let key = document.getElementById('key');
    let user = document.getElementById('user');
    let tab = document.getElementById('tab');
    let info = document.getElementById('info');


    
    key.style.display = 'none';

 

  tab.addEventListener('click', function() {
            if (tab.innerHTML === "Admin Sign up") {
                key.style.display = "block";
                tab.innerHTML = "User Sign up";
                info.innerHTML = "Sign up: Admin";
            } else if (tab.innerHTML === "User Sign up") {
                key.style.display = "none";
                info.innerHTML = "Sign up";
                tab.innerHTML = "Admin Sign up";
            }
        });
    










})

function displayFileName() {
    var input = document.getElementById('file-upload');
    var fileNameDisplay = document.getElementById('file-upload-filename');

    if (input.files && input.files.length > 0) {
        fileNameDisplay.textContent = input.files[0].name;
    } else {
        fileNameDisplay.textContent = '';
    }
}
function handleImageChange() {
    const fileInput = document.getElementById('image-upload');
    const img = document.getElementById('profile-img');

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
            img.src = e.target.result;
        };

        reader.readAsDataURL(fileInput.files[0]);
    }
}
function triggerFileInput() {
    document.getElementById('image-upload').click();
}
let pfInfo = document.getElementById('pf');
let save = document.getElementById('save');

let edit = document.getElementById('edit');
let image = document.getElementById('image-upload');
let full_name = document.getElementById('name');
let email = document.getElementById('email');
let username = document.getElementById('username');
let birth_date = document.getElementById('birth_date');
let hid = document.getElementById("hid")
let timer = document.getElementById("timer")

timer.style.display = "none"

save.style.display = "none"
hid.style.display = "none"
edit.addEventListener('click', function() {
    edit.style.display = "none";
    save.style.display = "block";
    pfInfo.style.display = "none"
    hid.style.display = "block";
})

save.addEventListener('click', function(event) {
    event.preventDefault();

    edit.style.display = "block";
    save.style.display = "none";
    pfInfo.style.display = "block"
    hid.style.display = "none";
    timer.style.display = "block"
    setTimeout(function() {
        window.location.href = "/v1/";
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

    fetch('edit', {
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
