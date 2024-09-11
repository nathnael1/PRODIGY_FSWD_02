document.addEventListener('DOMContentLoaded', function() {
let editUserIcons = document.querySelectorAll(".pedit");
let pshow = document.querySelectorAll(".pshow");
let pdelete = document.querySelectorAll(".pdelete");
let popup = document.getElementById("popup");
let warning = document.getElementById("warning");
let cwarning = document.getElementById("cwarning");
let confirm = document.getElementById("confirm");
let cache = ""
popup.style.display = "none"
confirm.style.display = "none"
editUserIcons.forEach(icon => {
    icon.addEventListener('click', function(event) {

        let username = event.target.getAttribute("data-username");
        window.location.href = `/v1/editUser/${username}`;
    });
});

pshow.forEach(icon => {
    icon.addEventListener('click', function(event) {
        let username = event.target.getAttribute("data-username");
        window.location.href = `/v1/show/${username}`;
    });
});
pdelete.forEach(icon => {
    icon.addEventListener('click', function(event) {
        let username = event.target.getAttribute("data-username");
        popup.style.display = "block"
        popup.classList.remove('disabled')
        warning.innerHTML = `Are you sure you want to delete <strong>${username}</strong>`;
        cache = username    
    });
});
cwarning.addEventListener('click', function() {
    popup.style.display = "none"
    confirm.classList.remove('disabled')
    confirm.style.display = "block"
    setTimeout(function() {
        window.location.href = `/v1/delete/${cache}`;
    },4000)
})





})