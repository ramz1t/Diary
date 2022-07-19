async function submit() {
    var type = $.cookie("type");
    var pass = document.getElementById("password").value;
    var subpass = document.getElementById("repeatpassword").value;
    var email = document.getElementById("email").value;
    var key = document.getElementById("secretkey").value;
    if (email.search("@") === -1 || email === "") {
        alert('Not email')
        return;
    }
    if (pass === "") {
        alert('Not password')
        return;
    }
    if (pass !== subpass) {
        alert('miss match')
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
        alert('created');
    } else {
        await alertError(response);
    }

}


function openLoginPage(type) {
    window.open(`/${type}/login`, '_self')
}
