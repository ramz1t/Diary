async function login() {
    const type = localStorage.getItem('type');
    const pass = document.getElementById("password").value;
    const email = document.getElementById("email").value;
    const remember = $('#remember_me').is(':checked');
    const response = await fetch('/token', {
        method: 'POST',
        headers: {
            'accept': 'application/json'
        },
        body: new URLSearchParams({
            'username': email,
            'password': pass,
            'client_id': type,
            'client_secret': remember
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

addEventListener('keyup', function (e) {
    if(e.keyCode === 13){
        login();
    }
})