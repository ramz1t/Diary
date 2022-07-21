async function login() {
    var type = localStorage.getItem('type');
    var pass = document.getElementById("password").value;
    var email = document.getElementById("email").value;
    var response = await fetch('/token/' + type, {
        method: 'POST',
        headers: {
            'accept': 'application/json'
        },
        body: new URLSearchParams({
            'username': email,
            'password': pass
        })
    });
    if (response.ok) {
        window.open('/' + type, '_self');
    } else {
        await alertError(response);
    }
    if (type === 'admin') {
        document.cookie = "school_id=" + email;
    }
}

function openRegisterPage(type) {
    window.open(`/${type}/register`, '_self')
}
