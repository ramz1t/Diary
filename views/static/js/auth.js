async function submit() {
    var type = localStorage.getItem('type');
    var pass = document.getElementById("password").value;
    var subpass = document.getElementById("repeatpassword").value;
    var email = document.getElementById("email").value;
    var key = document.getElementById("secretkey").value;
    if (email.search("@") === -1 || email === "") {
        Swal.fire({
            text: 'Not Email',
            position: 'top',
            timer: 2000
        })
        return;
    }
    if (pass === "") {
        Swal.fire({
            text: 'Not password',
            position: 'top',
            timer: 2000
        })
        return;
    }
    if (pass !== subpass) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Miss match',
            position: 'top',
            timer: 2000
        })
        return;
    }

    var response = await fetch(`/execute/${type}/create`, {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'password': pass,
            'email': email,
            'key': key
        })
    });

    if (response.ok) {
        Swal.fire({
            icon: 'success',
            text: 'Created!',
            position: 'top',
            timer: 2000
        })
    } else {
        await alertError(response);
    }

}


function openLoginPage(type) {
    window.open(`/${type}/login`, '_self')
}
