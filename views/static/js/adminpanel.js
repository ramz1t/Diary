async function addGroup() {
    var groupName = document.getElementById("groupname").value;
    var response = await fetch('/add_group_to_db', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'name': groupName
        })
    });
    if (response.ok) {
        window.open('/admin/add_group', '_self');
    } else {
        alert('error');
    }
}

async function addKey() {
    var name = document.getElementById('name');
    var surname = document.getElementById('surname');
    if (document.querySelector('input[name="group"]:checked') != null) {
        var group = document.querySelector('input[name="group"]:checked').value;
    } else {
        return
    }
    var response = await fetch('/add_key_to_db', {
                            method: 'POST',
                            headers: {
                                'accept': 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                'name': name.value,
                                'surname': surname.value,
                                'group': group
                            })
                        });
    if (response.ok) {
        window.open('/admin/add_key', '_self');
    } else {
        alert('error');
    }
}

function download(value) {
    window.open(`download/${value}`)
}

function logout() {
    window.open( SERVER_DOMAIN + '/admin/login', '_self');
    document.cookie = 'access_token=; expires=-1;';
}

async function changePassword() {
    var new_pass = document.getElementById("New_pass").value;
    var old_pass = document.getElementById("Old_pass").value;
    var repeat_new_pass = document.getElementById("Repeat_new_pass").value;
    if (new_pass !== repeat_new_pass) {
        document.getElementById("New_pass").classList.add('is-invalid');
        document.getElementById("Repeat_new_pass").classList.add('is-invalid');
        return;
    }
    var response = await fetch(SERVER_DOMAIN + '/change_password', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'new_password': new_pass,
            'old_password': old_pass
        })
    });
}

async function manageGroups(){
    window.open('/admin/managegroups', '_self')
}
