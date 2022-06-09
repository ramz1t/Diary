async function submit() {
    const toasterror = document.getElementById('toast');
    const toast = new bootstrap.Toast(toasterror);
    var pass = document.getElementById("password").value;
    var subpass = document.getElementById("repeatpassword").value;
    var email = document.getElementById("email").value;
    var name = document.getElementById("name").value;
    if (email.search("@") == -1 || email == "") {
        document.getElementById("email").classList.add('is-invalid');
        return;
    }
    if (pass == "") {
        document.getElementById("password").classList.add('is-invalid');
        return;
    }
    if (pass != subpass) {
        document.getElementById("password").classList.add('is-invalid');
        document.getElementById("repeatpassword").classList.add('is-invalid');
        return;
    }
    if (document.querySelector('input[name="gender"]:checked') != null) {
        var gender = document.querySelector('input[name="gender"]:checked').value;
    } else {
        return;
    }
    var response = await fetch('create_student', {
                            method: 'POST',
                            headers: {
                                'accept': 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                'email': email,
                                'password': pass
                            })
    });
    if (!response.ok) {
        if (response.status == '400') {
            alert('Invalid data');
        } else if (response.status == '409') {
            document.getElementById("alert-message").innerHTML = 'Email already in use'
            toast.show()
        }
    } else {
        alert("все работает")
    }
}
