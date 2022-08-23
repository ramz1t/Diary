async function callServer(url, data, method) {
    return await fetch(url, {
        method: method,
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
}

function executeScripts(page) {
    if (page === 'manage_groups') {
        loadSchedule('load', '0');
    }
}

function writeStorage(data) {
    for (let i = 0; i < data.length; i++) {
        localStorage.setItem(data[i][0], data[i][1]);
    }
}

function logout() {
    const type = localStorage.getItem('type');
    document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.open(`/${type}/login`, '_self');

}

function checkCredentials(status) {
    const timeout = 2000;
    if (status === 401) {
        Swal.fire({
            text: 'Your session has expired, please log in again',
            timer: timeout
        });
        setTimeout(logout, timeout)
        throw 'credentials error 401'
    }

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
    alert(text);
}

async function loadPage(type, page) {
    let user_id = localStorage.getItem('user_id');
    if (page === 'load') {
        page = localStorage.getItem(`${type}_page`);
    } else {
        localStorage.setItem(`${type}_page`, page);
    }
    if (page !== null) {
        let data = {
            'user_id': user_id,
            'type': type,
            'page': page
        };
        let response = await callServer('/load_page/', data, 'PATCH');
        if (response.ok) {
            let wrapper = document.getElementById('wrapper');
            response = await response.text();
            wrapper.innerHTML = '';
            wrapper.innerHTML = response;
        } else {
            checkCredentials(response.status)
        }
        executeScripts(page);
    }
}

function deleteFromDB(id, model) {
    callServer(`/${model}/delete`, {'id': id}, 'POST').then((response) => {
        checkCredentials(response.status);
        alertError(response);
    }).then(() => {
        window.location.reload(true)
    })
}