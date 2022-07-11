async function submit() {
    var type = $.cookie("type");
        var pass = document.getElementById("password").value;
        var subpass = document.getElementById("repeatpassword").value;
        var email = document.getElementById("email").value;
        var key = document.getElementById("secretkey").value;
        if (email.search("@") == -1 || email == "") {
            alert('Not email')
            return;
        }
        if (pass == "") {
            alert('Not password')
            return;
        }
        if (pass != subpass) {
            alert('miss match')
            return;
        }

        var response = await fetch(SERVER_DOMAIN + `/execute/${type}/create`, {
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

        if (!response.ok) {
            if (response.status == '400') {
                alert('Invalid data');
            } else if (response.status == '409') {
                alert('error')
            }
        } else {
            alert("все работает")
        }

}


function openLoginPage(type) {
    window.open(SERVER_DOMAIN + `/${type}/login`, '_self')
}
