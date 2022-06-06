async function login() {
    var pass = document.getElementById("password").value;
    var email = document.getElementById("email").value;
    var response = await fetch('/token', {
        method: 'POST',
        headers: {
            'accept': 'application/json'
        },
        body: new URLSearchParams({
            'username': email,
            'password': pass
        })
    });
    if (response.status == '200') {
        alert('LOGIN DONE');
    } else {
        alert(response.status);
    }
}
