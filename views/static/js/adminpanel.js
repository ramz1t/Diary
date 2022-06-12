async function addGroup() {
    var groupName = document.getElementById("groupname").value;
    var response = await fetch('/add_group', {
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
        window.open('/admin', '_self');
    } else {
        alert('error');
    }
}


async function addKey() {
    var name = document.getElementById('name').value;
    var surname = document.getElementById('surname').value;
    if (document.querySelector('input[name="group"]:checked') != null) {
        var group = document.querySelector('input[name="group"]:checked').value;
    } else {
        return
    }
    var response = await fetch('/add_key', {
                            method: 'POST',
                            headers: {
                                'accept': 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                'name': name,
                                'surname': surname,
                                'group': group
                            })
                        });
    if (response.ok) {
        window.open('/admin', '_self')
    } else {
        alert('error');
    }
}

function download(value) {
    window.open(`download/${value}`)
}
