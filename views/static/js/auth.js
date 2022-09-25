async function submit() {
    var type = localStorage.getItem('type');
    var pass = document.getElementById("password");
    var subpass = document.getElementById("repeatpassword");
    var email = document.getElementById("email");
    var key = document.getElementById("secretkey");
    email.addEventListener('input',()=>{
        const emailBox = document.querySelector('.emailBox');
        const emailText = document.querySelector('.emailText');
        const emailPattern = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{1,63}$/;
        if (email.value.match(emailPattern)){
            emailBox.classList.add('valid');
            emailBox.classList.remove('invalid');
            emailText.innerHTML = "Your Email Address in Valid";
        }
        else{
            emailBox.classList.add('invalid');
            emailBox.classList.remove('valid');
            emailText.innerHTML = "Must be a valid email address.";
            return;
        }
    })
    pass.addEventListener("input", ()=> {
        const passBox = document.querySelector('.passBox');
        const passText = document.querySelector('.passText');
        const passwordPattern = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}/;
        if (pass.value.match(passwordPattern)) {
            passBox.classList.add('valid');
            passBox.classList.remove('invalid');
            passText.innerHTML = "Your Password in Valid";
        } else {
            passBox.classList.add('invalid');
            passBox.classList.remove('valid');
            passText.innerHTML = "Your password must be at least 8 characters as well as contain at least one uppercase, one lowercase, and one number.";
            return;
        }
    })
    subpass.addEventListener('input', ()=> {
        const subPassBox = document.querySelector('.subPassBox');
        const subPassText = document.querySelector('.subPassText');
        if (pass.value === subpass.value){
            subPassBox.classList.add('valid');
            subPassBox.classList.remove('invalid');
            subPassText.innerHTML = "Passwords match"
        }
        else {
            subPassBox.classList.add('invalid');
            subPassBox.classList.remove('valid');
            subPassText.innerHTML = "Miss match";
            return;
        }
    })
    var response = await fetch(`/execute/${type}/create`, {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'password': pass.value,
            'email': email.value,
            'key': key.value
        })
    });

    if (response.ok) {
        Swal.fire({
            icon: 'success',
            text: 'Created!',
            position: 'top',
            timer: 2000,
            showConfirmButton: false,
        })
    } else {
        await alertError(response);
    }

}


function openLoginPage(type) {
    window.open(`/${type}/login`, '_self')
}
