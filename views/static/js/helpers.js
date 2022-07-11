function logout() {
    var type = $.cookie("type");
    window.open(`/${type}/login`, '_self');
    document.cookie = 'access_token=; expires=-1;';
}

async function changePassword() {
    var type = $.cookie("type");
    var new_pass = document.getElementById("New_pass").value;
    var old_pass = document.getElementById("Old_pass").value;
    var repeat_new_pass = document.getElementById("Repeat_new_pass").value;
    if (new_pass !== repeat_new_pass) {
        document.getElementById("New_pass").classList.add('is-invalid');
        document.getElementById("Repeat_new_pass").classList.add('is-invalid');
        return;
    }
    var response = await fetch('/change_user_password', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'new_password': new_pass,
            'old_password': old_pass,
            'type': type
        })
    });
    var text = await response.json();
    alert(text);
}

async function changeEmail() {
    var type = $.cookie("type");
    var new_email = document.getElementById('New_email').value;
    var old_email = document.getElementById('Old_email').value;
    var response = await fetch('/change_user_email', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'type': type,
            'new_email': new_email,
            'old_email': old_email
        })

    });
    var text = await response.json();
    alert(text)
}

async function loadPage(type, page) {
    var school_id = $.cookie("school_id");
    if (page === 'load') {
        page = $.cookie("page");
    } else {
        document.cookie = "page=" + page;
    }
    if (page !== undefined) {
        var response = await fetch('http://127.0.0.1:8003/load_page/', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'school_id': school_id,
                'type': type,
                'page': page
            })
        });
        if (response.ok) {
            var wrapper = document.getElementById('wrapper');
            response = await response.text();
            wrapper.innerHTML = '';
            wrapper.innerHTML = response;
        }
    }
}